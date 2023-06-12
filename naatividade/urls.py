
from django.contrib import admin
from django.urls import path

from naatividade.core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('', views.processar_formulario),
]
