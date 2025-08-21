from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Usuario, OTP


class FluxoAccountsTests(TestCase):
    def test_fluxo_registro_otp_ativacao_e_definir_senha(self):
        resp = self.client.post(reverse("accounts:registro"), {
            "first_name": "Maria",
            "last_name": "Silva",
            "email": "maria@example.com",
        })
        self.assertEqual(resp.status_code, 302)
        user = Usuario.objects.get(email="maria@example.com")
        self.assertFalse(user.is_active)

        otp = OTP.objects.filter(user=user).latest("criado_em")
        self.assertTrue(otp.esta_valido())

        # Sessão mantém o email pendente; confirma apenas com o código
        session = self.client.session
        session["pending_email"] = user.email
        session.save()

        resp = self.client.post(reverse("accounts:confirmar_otp"), {"code": otp.code})
        self.assertEqual(resp.status_code, 302)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

        resp = self.client.post(reverse("accounts:definir_senha"), {
            "senha1": "NovaSenha123!",
            "senha2": "NovaSenha123!",
        })
        self.assertEqual(resp.status_code, 302)
        user.refresh_from_db()
        self.assertFalse(user.must_change_password)

# Create your tests here.
