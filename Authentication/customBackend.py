from django.contrib.auth.backends import ModelBackend
from .models import userAuth

class PasswordlessAuthBackend(ModelBackend):
   
    def authenticate(self,request, id):
        try:
            return userAuth.objects.get(id=id)   
        except userAuth.DoesNotExist:
            return None

    def get_user(self, id):
        try:   
            return userAuth.objects.get(id=id)
        except userAuth.DoesNotExist:
            return None