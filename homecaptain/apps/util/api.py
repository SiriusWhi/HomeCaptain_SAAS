from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, status, viewsets, permissions

from django.apps import apps
from django.db.models import FieldDoesNotExist
from django.conf import settings

from .tasks import generic_send_email, generic_send_raw_email

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class HCRecordCreateGenericViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    MODELS_TO_BE_SANITIZED = {
        'address': ('util', 'Address'),
        'user': ('hcauth', 'HomeCaptainUser'),
        'loan_officer': ('lender', 'LoanOfficer'),
        'lender': ('lender', 'Lender'),
        'realtor': ('realtor', 'Realtor'),
        'broker': ('realtor', 'Broker'),
        'requirements': ('requirement', 'Requirement'),
    }

    def _modify_email_for_debug(self, email):
        if settings.DEBUG and email.split('@'):
            return email.split('@')[0] + '@example.org'
        else:
            return email

    def _sanitize_record(self, record, Model):
        new_record = {}
        for k,v in record.items():
            if k in self.MODELS_TO_BE_SANITIZED:
                is_list = isinstance(v, list) #requirement
                if is_list:
                    v = v[0]
                model = self.MODELS_TO_BE_SANITIZED[k]
                model = apps.get_model(app_label=model[0], model_name=model[1])
                #print("calling sanitize_record on %s" % model.__name__)
                #DFTraversal
                v = self._sanitize_record(v, model)
                if is_list:
                    v = [v, ]
            else:
                try:
                    model_field = Model._meta.get_field(k)
                    internal_type = model_field.get_internal_type()
                    
                    if v in [None, '']:
                        if internal_type in ['CharField', 'TextField']:
                            v = ''
                            if k=='country' and internal_type == 'CharField':
                                v = 'US'
                        elif internal_type == 'IntegerField':
                            if model_field.choices:
                                continue
                            v = 0
                        elif internal_type == 'BooleanField':
                            v = False
                        elif internal_type == 'DecimalField':
                            continue #v = DECIMAL_DEFAULT
                        elif internal_type == 'FloatField':
                            v = 0.0
                    elif k.startswith('website'):
                        if not v.startswith('http'):
                            v = 'https://' + v
                    elif k.startswith('email') and settings.DEBUG:
                        v = self._modify_email_for_debug(v)
                    elif k.startswith('phone') and settings.DEBUG:
                        v = '1234567890'
                    elif k == 'state':
                        v = v[:2].upper()
                except (FieldDoesNotExist, KeyError):
                    pass
            if k == 'zip':
                k = 'postalcode'
            elif k == 'postalCode':
                k = 'postalCode'
            new_record[k] = v
        return new_record


class EmailSendGenericView(APIView):
    sender_type = 'realtor'

    def get(self, request, receiver_type=None):
        return Response({
            'fields': ('uid', 'subject', 'body'),
            'extra info': 'The `uid` in fields can be a `single customer.user.uid` or a list of `customer.user.uid` (NOT `customer.uid`)',
            'method': 'POST'
        })
    
    def post(self, request, receiver_type=None):
        if receiver_type:
            errors = {}
            receiver_user_uids = request.data.get('uid', [])
            if not receiver_user_uids:
                errors['uid'] = "receiver list is empty"
            subject = request.data.get('subject', '')
            if not subject:
                errors['subject'] = "subject is empty"
            body = request.data.get('body', '')
            if not body:
                errors ['body'] = "body is empty"
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            
            if not isinstance(receiver_user_uids, list):
                receiver_user_uids = [receiver_user_uids]

            sender_user_uid = request.user.uid

            #'lender']:#FIXME:lender model does not have email!!!
            if receiver_type == 'broker': 
                Model = apps.get_model('realtor', 'Broker')
                receiver_emails = list(Model.objects.filter(uid__in=receiver_user_uids).\
                                       values_list('email', flat=True))
                generic_send_raw_email.delay(
                    sender_user_uid, receiver_emails,
                    subject, body, 'contact')
            else:
                generic_send_email.delay(
                    sender_user_uid, self.sender_type, receiver_user_uids,
                    receiver_type, subject, body, 'contact')
                    
            return Response({
                'status': 'Email sent to task scheduler'
            })
