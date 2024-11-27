from django.contrib.auth.backends import ModelBackend
from accounts.models import *


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, phone=None, password=None, **kwargs):
        if phone is None:
            phone = kwargs.get(User.USERNAME_FIELD)
        if phone is None or password is None:
            return

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None