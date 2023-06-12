from django.http import HttpResponse
from django.shortcuts import render
from .models import Ativo

# Create your views here.


def index(request):
    lista_ativos = Ativo.object.filter(active=True)
    context = {'objectList': lista_ativos}
    return render(request, "index.html", context)

def processar_formulario(request):
    return
