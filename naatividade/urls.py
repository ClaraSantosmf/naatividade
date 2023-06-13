from django.contrib import admin
from django.urls import path

from naatividade.core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path(
        "cadastrar/",
        views.cadastrar_monitoramento,
        name="cadastrar",
    ),
]
