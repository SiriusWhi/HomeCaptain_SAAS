from django.contrib.auth.hashers import check_password
from .models import HomeCaptainUser


class SwaggerBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = HomeCaptainUser.objects.get(username=username)
        except:
            return None
        if check_password(password, user.password):
            return user
        return None

    def get_user(self, user_id):
        try:
            user = HomeCaptainUser.objects.get(id=user_id)
        except:
            return None
        return user

