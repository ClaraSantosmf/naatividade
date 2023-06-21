from zoneinfo import ZoneInfo
import pytest
from unittest import mock
import datetime as dt
import time_machine
from naatividade.core.models import Ativo, Email, Monitoramento, Historico
from naatividade.core.svc.mail_svc import (
    send_mail_alerta_venda,
    send_mail_alerta_compra,
)
from ..svc.api_svc import confere_e_atualiza_preco_de_ativo_na_api

BR_TIME = ZoneInfo("America/Sao_Paulo")


@pytest.fixture
def mock_db_alerta_venda(time_machine):
    time_machine.move_to(dt.datetime(1999, 9, 9, 15, 0, tzinfo=BR_TIME))
    timedelta_atual = dt.datetime.now()
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    email_azul = Email.objects.create(email="destinatario_azul@gmail.com")
    ativo_petrobras = Ativo.objects.create(nome="Petrobras", symbol="PETR3")
    ativo_azul = Ativo.objects.create(nome="Azul SA", symbol="AZUL4")
    Monitoramento.objects.create(
        ativo=ativo_petrobras,
        min_value=1,
        max_value=1.4,
        email=email_primeiro,
        schedule=8,
        last_view=timedelta_atual - dt.timedelta(minutes=5),
        next_view=timedelta_atual - dt.timedelta(minutes=8)
    )
    Monitoramento.objects.create(
        ativo=ativo_petrobras,
        min_value=0.50,
        max_value=2.20,
        email=email_segundo,
        schedule=5,
        last_view=timedelta_atual - dt.timedelta(minutes=10),
        next_view=timedelta_atual - dt.timedelta(minutes=5)
    )
    Monitoramento.objects.create(
        ativo=ativo_azul,
        min_value=15,
        max_value=20,
        email=email_azul,
        schedule=10,
        last_view=timedelta_atual - dt.timedelta(minutes=5),
        next_view=timedelta_atual + dt.timedelta(minutes=5)
    )
    Historico.objects.create(ativo=ativo_petrobras, valor=1.4)
    Historico.objects.create(ativo=ativo_azul, valor=19.87)
    return

@pytest.fixture
def mock_db_alerta_compra(time_machine):
    time_machine.move_to(dt.datetime(1999, 9, 9, 15, 0, tzinfo=BR_TIME))
    timedelta_atual = dt.datetime.now()
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    ativo_magalu = Ativo.objects.create(nome="Magalu", symbol="MGLU3")
    monitoramento_um = Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=2.0, max_value=4, email=email_primeiro, schedule=5,
        last_view=dt.datetime.now() - dt.timedelta(minutes=10),
        next_view=dt.datetime.now() - dt.timedelta(minutes=5)
    )
    monitoramento_dois = Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=1.50, max_value=3.20, email=email_segundo, schedule=5,
        last_view=timedelta_atual.now() - dt.timedelta(minutes=10),
        next_view=timedelta_atual.now() - dt.timedelta(minutes=5)
    )
    Historico.objects.create(ativo=ativo_magalu, valor=2.0)
    yield [monitoramento_um, monitoramento_dois]


def test_send_mail_alerta_venda(db, mock_db_alerta_venda):
    ativo_petrobras = mock_db_alerta_venda
    datatuple = [
        (
            "Está na hora de vender Petrobras",
            "O ativo Petrobras está custando 1.40! Exatamente o preço de venda estabelecido no seu alerta NaAtividade. Alerta -> 1.40",
            "naatividade@gmail.com",
            ["destinatario@gmail.com"],
        ),
        (
            "Está na hora de vender Petrobras",
            "O ativo Petrobras está custando 1.40! Está maior que o preço de venda estabelecido no seu alerta NaAtividade. Alerta -> 2.20",
            "naatividade@gmail.com",
            ["destinatario2@gmail.com"],
        ),
    ]
    ativo_petrobras = Monitoramento.objects.select_related('ativo', 'email').filter(next_view__lte=dt.datetime.now())
    with mock.patch(
        "naatividade.core.svc.mail_svc.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_venda(ativo_petrobras)
    mock_send_mass_mail.call_count == 2
    mock_send_mass_mail.assert_called_with(datatuple, fail_silently=False)


def test_nao_send_mail_alerta_vendaOI(db, mock_db_alerta_venda):
    with mock.patch(
        "naatividade.core.svc.mail_svc.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_venda([])
    mock_send_mass_mail.assert_not_called()


def test_send_mail_alerta_compra(db, mock_db_alerta_compra):
    monitoramentos_validos = mock_db_alerta_compra
    datatuple = [
        (
            "Está na hora de comprar Magalu",
            "O ativo Magalu está custando 2.00! Exatamente o preço de compra estabelecido no seu alerta NaAtividade. Alerta -> 2.0",
            "naatividade@gmail.com",
            ["destinatario@gmail.com"],
        ),
        (
            "Está na hora de comprar Magalu",
            "O ativo Magalu está custando 2.00! Menor que o preço de compra estabelecido no seu alerta NaAtividade. Alerta -> 1.5",
            "naatividade@gmail.com",
            ["destinatario2@gmail.com"],
        ),
    ]

    with mock.patch(
        "naatividade.core.svc.mail_svc.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_compra(monitoramentos_validos)
    mock_send_mass_mail.call_count == 2
    mock_send_mass_mail.assert_called_with(datatuple, fail_silently=False)


def test_nao_send_mail_alerta_compra_sem_parametro(db, mock_db_alerta_compra):
    with mock.patch(
        "naatividade.core.svc.mail_svc.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_compra([])
    mock_send_mass_mail.assert_not_called()
