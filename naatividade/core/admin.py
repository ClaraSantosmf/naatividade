from django.contrib import admin
from .models import Ativo, Monitoramento, Email, Historico

admin.site.register(Ativo)
admin.site.register(Monitoramento)
admin.site.register(Email)
admin.site.register(Historico)
