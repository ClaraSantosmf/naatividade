import pytest
from django.db.models import Q, F
from django.db.models.functions import Mod
from ..models import Monitoramento, Ativo, Historico, Email
from django.db.models import QuerySet


@pytest.fixture
def mock_banco_para_filtro():
    email = Email.objects.create(email="destinatario@gmail.com")
    ativo_azul = Ativo.objects.create(nome="Azul SA", symbol="AZUL4")
    historico = Historico.objects.create(ativo=ativo_azul, valor=19.87)
    monitoramento_filtrado = Monitoramento.objects.create(
        ativo=ativo_azul, min_value=18, max_value=20, email=email, schedule=5
    )
    monitoramento_nao_filtrado = Monitoramento.objects.create(
        ativo=ativo_azul, min_value=18, max_value=20, email=email, schedule=63
    )
    yield historico, monitoramento_filtrado


def test_query_monitoramento(db, mock_banco_para_filtro):
    historico_banco, monitoramento_filtrado_banco = mock_banco_para_filtro
    valor = 5
    monitoramentos = (
        Monitoramento.objects.annotate(schedule_mod=Mod("schedule", valor))
        .filter(Q(schedule_mod=0) | Q(schedule_mod=F("schedule")))
        .select_related("ativo")
    )
    monitoramento_ativos_ids = monitoramentos.values_list("ativo__id", flat=True)
    historicos_relacionados = Historico.objects.filter(
        ativo_id__in=monitoramento_ativos_ids
    )
    assert float(historicos_relacionados[0].valor) == historico_banco.valor
    assert isinstance(monitoramentos, QuerySet)
    assert len(monitoramentos) == 1
    assert monitoramentos[0] == monitoramento_filtrado_banco
