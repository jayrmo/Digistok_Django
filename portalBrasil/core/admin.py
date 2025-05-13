from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# class UsuarioAdmin(UserAdmin):
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ('cpf', 'data_nascimento', 'telefone')})
#     )
    
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (None, {'fields': ('cpf', 'data_nascimento', 'telefone')})
#     )
    
#     search_fields = UserAdmin.search_fields + ('cpf', 'telefone')

admin.site.register(Usuario)