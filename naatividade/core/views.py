from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .svc import monitoramento_svc
from .forms import MonitoramentoForm
from .models import Ativo, Monitoramento


def ativo_list(request):
    lista_ativos = Ativo.objects.all()
    context = {"object_list": lista_ativos}
    return render(request, "index.html", context)


def index(request):
    monitoramento_ativos = Monitoramento.objects.filter(active=True).select_related(
        "ativo"
    )
    context = {"object_list": monitoramento_ativos}
    return render(request, "index.html", context)


def cadastrar_monitoramento(request):
    form = MonitoramentoForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        monitoramento_svc.validacao_cadastramento(form)
        return redirect(reverse("index"))
    context = {"form": form}
    return render(request, "monitoramento_crud.html", context)
