from django import forms

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.template import loader

from apps.util.tasks import system_email
from apps.util.utils import get_logger
from apps.util.picklists import USER_TYPE_CHOICES

UserModel = get_user_model()

class HCPasswordResetForm(PasswordResetForm):
    logger = get_logger('HCPasswordResetForm')

    #def save(self, *args, **kwargs):
    #    kwargs['email_template_name'] = 'hcauth/registration/password_reset_email.html'
    #    return super(HCPasswordResetForm, self).save(*args, **kwargs)

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        ##send only one email to one email address
        users = [u for u in active_users if u.has_usable_password()]

        self.logger.debug(users)
        
        filtered_users = []
        if email.split('@')[1] in ['homecaptain.com', 'roostify.com']:
            ##if the domain of email is among homecaptain or roostify
            for user in users:
                if user.user_type in picklists.NON_HC_STAFF_USER_TYPES:
                    ##and/but the user type is non HC staff (admin or concierge)
                    continue
                else:
                    filtered_users.append(user)
        else:
            filtered_users = users

        self.logger.debug(filtered_users)
                    
        return filtered_users

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        self.logger.debug(context)
        user = context.pop('user')
        context['user_uid'] = user.uid
        system_email.delay(to_email, subject, '', 'password_reset_email', context=context)
