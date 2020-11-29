import traceback

from django.conf import settings

from anymail.backends.sendgrid import EmailBackend
from anymail.exceptions import AnymailError

from .models import HCOutGoingEmail
from .utils import get_logger


class HCSendgridEmailBackend(EmailBackend):
    logger = get_logger('HCSendgridEmailBackend')

    def send_messages(self, email_messages):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        # This API is specified by Django's core BaseEmailBackend
        # (so you can't change it to, e.g., return detailed status).
        # Subclasses shouldn't need to override.

        num_sent = 0
        if not email_messages:
            return num_sent

        created_session = self.open()

        try:
            for message in email_messages:
                
                hc_outgoing_email = HCOutGoingEmail()
                hc_outgoing_email.subject = message.subject
                hc_outgoing_email.to = message.recipients()
                
                if settings.DEBUG:
                    self.logger.debug("setting dev emails")
                    message.to = settings.DEV_EMAILS

                self.logger.debug(str(message.recipients()))
                
                if hasattr(message, 'hc_template_name') and getattr(message, 'hc_template_name', None):
                    hc_outgoing_email.template_name = message.hc_template_name
                if hasattr(message, 'hc_created_by') and getattr(message, 'hc_created_by', None):
                    hc_outgoing_email.created_by = message.hc_created_by
                    
                try:
                    sent = self._send(message)
                    if message.anymail_status.message_id:
                        hc_outgoing_email.anymail_message_id = message.anymail_status.message_id
                except AnymailError:
                    self.logger.critical(traceback.format_exc())
                    hc_outgoing_email.sent = False
                    hc_outgoing_email.error = str(traceback.format_exc())
                    
                    if self.fail_silently:
                        sent = False
                    else:
                        raise
                finally:
                    hc_outgoing_email.save()
                    
                if sent:
                    num_sent += 1
        finally:
            if created_session:
                self.close()

        return num_sent

