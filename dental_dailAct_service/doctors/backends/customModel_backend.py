from django.contrib.auth.backends import ModelBackend
from doctors.models import User

class DoctorBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = User()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                return None
        if user.check_password(password):
            return user
    def get_user(self, user_id):
        UserModel = User()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
