from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import MonitoramentoForm
from .models import Ativo, Monitoramento


def ativo_list(request):
    lista_ativos = Ativo.objects.all()
    context = {"object_list": lista_ativos}
    return render(request, "index.html", context)


def index(request):
    monitoramento_ativos = Monitoramento.objects.filter(active=True)
    context = {"object_list": monitoramento_ativos}
    return render(request, "index.html", context)


def cadastramento_de_monitoramento(request):
    form = MonitoramentoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse("index"))
    context = {"form": form}
    return render(request, "monitoramento_crud.html", context)
