from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from utils.validacoes.uuid7 import uuid7


class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    email = models.EmailField(unique=True)
    must_change_password = models.BooleanField(default=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


class OTP(models.Model):
    class OTPType(models.TextChoices):
        REGISTRO = "registro", "Registro"

    user = models.ForeignKey("accounts.Usuario", on_delete=models.CASCADE, related_name="otps")
    code = models.CharField(max_length=10)
    tipo = models.CharField(max_length=32, choices=OTPType.choices)
    expira_em = models.DateTimeField()
    usado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def esta_valido(self) -> bool:
        if self.usado:
            return False
        return timezone.now() <= self.expira_em

    def marcar_usado(self) -> None:
        self.usado = True
        self.save(update_fields=["usado"])

