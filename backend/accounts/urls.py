from django.urls import path
from . import views


app_name = "accounts"

urlpatterns = [
    path("registro/", views.registro_view, name="registro"),
    path("otp/confirmar/", views.confirmar_otp_view, name="confirmar_otp"),
    path("otp/reenviar/", views.reenviar_otp_view, name="reenviar_otp"),
    path("ativar/", views.ativar_view, name="ativar"),
    path("senha/definir/", views.definir_senha_view, name="definir_senha"),
    path("login/", views.login_view, name="login"),
]


