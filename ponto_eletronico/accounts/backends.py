from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CPFBackend(ModelBackend):
    """
    Backend de autenticação customizado que utiliza CPF em vez de username
    """

    def authenticate(self, request, cpf=None, password=None, **kwargs):
        try:
            user = User.objects.get(cpf=cpf)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
