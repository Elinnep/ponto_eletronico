from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('cpf', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email')}),
        ('Informações Profissionais', {'fields': ('matricula',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cpf', 'email', 'first_name', 'last_name', 'matricula', 'password1', 'password2'),
        }),
    )
    list_display = ('cpf', 'first_name', 'last_name', 'email', 'matricula', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('cpf', 'email', 'first_name', 'last_name', 'matricula')
    ordering = ('cpf',)
    filter_horizontal = ('groups', 'user_permissions',)
