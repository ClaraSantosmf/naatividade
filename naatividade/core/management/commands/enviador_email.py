from django.utils import timezone
from django.db.models import F, Q
from django.db.models.functions import Mod
from svc.api_svc import confere_preco_de_ativo_na_api
from models import Monitoramento, Historico
import djclick as click


@click.command()
def command():
    horario_brasilia = timezone.now()
    minutos = horario_brasilia.minute
    monitoramentos = (
        Monitoramento.objects.annotate(schedule_mod=Mod("schedule", minutos))
        .filter(Q(schedule_mod=0) | Q(schedule_mod=F("schedule")))
        .select_related("ativo")
    )
    lista_symbols_ativos_monitorados = monitoramentos.values_list(
        "ativo__symbol", flat=True
    )
    historicos_relacionados = Historico.objects.filter(
        ativo_symbol__in=lista_symbols_ativos_monitorados
    )
    response = confere_preco_de_ativo_na_api(
        lista_symbols_ativos_monitorados, historicos_relacionados
    )
