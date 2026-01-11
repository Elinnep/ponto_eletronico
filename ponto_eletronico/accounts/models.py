from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF é obrigatório")
        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(cpf, email, password, **extra_fields)


class User(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True)
    matricula = models.CharField(max_length=50, unique=True)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "matricula"]

    class Meta:
        db_table = "auth_user"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cpf})"

    def clean(self):
        super().clean()
        # Validação simples de CPF: apenas 11 dígitos numéricos
        if not self.cpf.isdigit() or len(self.cpf) != 11:
            raise ValidationError(
                {"cpf": "CPF deve conter exatamente 11 dígitos numéricos."}
            )
