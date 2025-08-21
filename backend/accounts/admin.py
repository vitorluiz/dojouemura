from django.contrib import admin
from .models import Usuario, OTP


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "is_active", "must_change_password")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "must_change_password", "is_staff", "is_superuser")


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tipo", "code", "usado", "expira_em", "criado_em")
    list_filter = ("tipo", "usado")
    search_fields = ("user__email", "code")

