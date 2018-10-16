from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
User = get_user_model()

class PhoneAuthenticationBackend:

    def authenticate(self, request, username=None, password=None):
        try:
             user = User.objects.get(phone=username)
             pwd_valid = user.check_password(password)
             if pwd_valid:            
                 return user
             return None
        except User.DoesNotExist:
            return None
        except ValueError: # for cases when email is given as username
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None