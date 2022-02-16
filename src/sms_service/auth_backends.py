from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Account


class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.password != password:
                user = None
        except User.DoesNotExist: 
            try:
                user = Account.objects.get(username=username, auth_id=password)
                user = User(username=username, password=password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            except Account.DoesNotExist:
                user = None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None