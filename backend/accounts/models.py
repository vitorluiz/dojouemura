from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from utils.validacoes.uuid7 import uuid7


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("O email é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        # superusuário não deve ser forçado a trocar a senha no login
        extra_fields.setdefault("must_change_password", False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    email = models.EmailField(unique=True)
    must_change_password = models.BooleanField(default=True)

    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UsuarioManager()


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

