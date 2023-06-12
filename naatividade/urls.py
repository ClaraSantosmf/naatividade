
from django.contrib import admin
from django.urls import path

from naatividade.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastramento', views.cadastramento_de_monitoramento, name='cadastramento_de_monitoramento')
]
