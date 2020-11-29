from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter, build_absolute_uri

class HCAccountAdapter(DefaultAccountAdapter):
    
    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse(
            "auth-api:account_confirm_email",
            args=[emailconfirmation.key])
        ret = build_absolute_uri(
            request,
            url)
        return ret
