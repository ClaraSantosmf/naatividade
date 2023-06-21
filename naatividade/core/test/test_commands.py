import pytest
from ..models import Monitoramento, Ativo, Historico, Email
import datetime as dt
from click.testing import CliRunner
from ..management.commands.enviador_email import command
import time_machine
from zoneinfo import ZoneInfo


br_time = ZoneInfo("America/Sao_Paulo")


@pytest.fixture()
@pytest.mark.django_db
@time_machine.travel(dt.datetime(1999, 9, 9, 15, 0, tzinfo=br_time))
def mock_banco_para_filtro_nova_logica():
    timedelta_atual = dt.datetime.now().astimezone(br_time)
    email = Email.objects.create(email="destinatario@gmail.com")
    ativo_azul = Ativo.objects.create(nome="Azul SA", symbol="AZUL4")
    historico = Historico.objects.create(ativo=ativo_azul, valor=19.87)
    monitoramento = Monitoramento.objects.create(
        ativo=ativo_azul,
        min_value=18,
        max_value=20,
        email=email,
        schedule=5,
        last_view=timedelta_atual,
        next_view=timedelta_atual + dt.timedelta(minutes=5)
    )

    return historico, monitoramento


@pytest.mark.django_db
def test_query_monitoramento_nova_logica(mock_banco_para_filtro_nova_logica):
    historico, monitoramento_filtrado_banco = mock_banco_para_filtro_nova_logica
    valor = 5
    monitoramento = Monitoramento.objects.first()
    assert monitoramento == monitoramento_filtrado_banco
    next_view_esperada = dt.datetime(1999, 9, 9, 15, 5, tzinfo=br_time)
    last_view_esperada = dt.datetime(1999, 9, 9, 15, 0, tzinfo=br_time)
    monitoramento == monitoramento_filtrado_banco
    assert monitoramento.next_view == next_view_esperada
    assert monitoramento.last_view == last_view_esperada

@pytest.mark.django_db
@time_machine.travel(dt.datetime(1985, 10, 26, 1, 24, tzinfo=br_time))
def test_acionar_commands_email(mock_banco_para_filtro_nova_logica):
    x = mock_banco_para_filtro_nova_logica
    runner = CliRunner()
    result = runner.invoke(command)
    assert result.exit_code == 1, result.output
