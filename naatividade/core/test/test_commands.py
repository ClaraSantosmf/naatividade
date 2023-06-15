import pytest
from unittest import mock
from naatividade.core.models import Ativo, Email, Monitoramento, Historico
from naatividade.management.commands.send_email import (
    send_mail_alerta_venda,
    send_mail_alerta_compra,
)


@pytest.fixture
def mock_fluxo_alerta_venda():
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    ativo_petrobras = Ativo.objects.create(nome="Petrobras", symbol="PETR3")
    Monitoramento.objects.create(
        ativo=ativo_petrobras, min_value=1, max_value=1.4, email=email_primeiro
    )
    Monitoramento.objects.create(
        ativo=ativo_petrobras, min_value=0.50, max_value=2.20, email=email_segundo
    )
    Historico.objects.create(ativo=ativo_petrobras, valor=1.4)
    yield ativo_petrobras


@pytest.fixture
def mock_fluxo_alerta_venda_sem_parametro():
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    ativo_petrobras = Ativo.objects.create(nome="Petrobras", symbol="PETR3")
    Monitoramento.objects.create(
        ativo=ativo_petrobras, min_value=1, max_value=1.4, email=email_primeiro
    )
    Monitoramento.objects.create(
        ativo=ativo_petrobras, min_value=0.50, max_value=4.99, email=email_segundo
    )
    Historico.objects.create(ativo=ativo_petrobras, valor=5.0)
    yield ativo_petrobras


@pytest.fixture
def mock_fluxo_alerta_compra():
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    ativo_magalu = Ativo.objects.create(nome="Magalu", symbol="MGLU3")
    Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=2, max_value=4, email=email_primeiro
    )
    Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=1.50, max_value=3.20, email=email_segundo
    )
    Historico.objects.create(ativo=ativo_magalu, valor=2)
    yield ativo_magalu


@pytest.fixture
def mock_fluxo_alerta_compra_sem_parametro():
    email_primeiro = Email.objects.create(email="destinatario@gmail.com")
    email_segundo = Email.objects.create(email="destinatario2@gmail.com")
    ativo_magalu = Ativo.objects.create(nome="Magalu", symbol="MGLU3")
    Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=2.00, max_value=4, email=email_primeiro
    )
    Monitoramento.objects.create(
        ativo=ativo_magalu, min_value=1.50, max_value=3.20, email=email_segundo
    )
    Historico.objects.create(ativo=ativo_magalu, valor=1.00)
    yield ativo_magalu


def test_send_mail_alerta_venda(db, mock_fluxo_alerta_venda):
    ativo_petrobras = mock_fluxo_alerta_venda
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

    with mock.patch(
        "naatividade.management.commands.send_email.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_venda(ativo_petrobras.id)
    mock_send_mass_mail.assert_called_once()
    mock_send_mass_mail.assert_called_once_with(datatuple, fail_silently=False)


def test_nao_send_mail_alerta_venda_sem_parametro(
    db, mock_fluxo_alerta_venda_sem_parametro
):
    ativo_petrobras = mock_fluxo_alerta_venda_sem_parametro
    with mock.patch(
        "naatividade.management.commands.send_email.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_venda(ativo_petrobras.id)
    mock_send_mass_mail.assert_not_called()


def test_send_mail_alerta_compra(db, mock_fluxo_alerta_compra):
    ativo_magalu = mock_fluxo_alerta_compra
    datatuple = [
        (
            "Está na hora de comprar Magalu",
            "O ativo Magalu está custando 2.00! Exatamente o preço de compra estabelecido no seu alerta NaAtividade. Alerta -> 2.00",
            "naatividade@gmail.com",
            ["destinatario@gmail.com"],
        ),
        (
            "Está na hora de comprar Magalu",
            "O ativo Magalu está custando 2.00! Menor que o preço de compra estabelecido no seu alerta NaAtividade. Alerta -> 1.50",
            "naatividade@gmail.com",
            ["destinatario2@gmail.com"],
        ),
    ]

    with mock.patch(
        "naatividade.management.commands.send_email.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_compra(ativo_magalu.id)
    mock_send_mass_mail.assert_called_once()
    mock_send_mass_mail.assert_called_once_with(datatuple, fail_silently=False)


def test_nao_send_mail_alerta_compra_sem_parametro(
    db, mock_fluxo_alerta_compra_sem_parametro
):
    ativo_magalu = mock_fluxo_alerta_compra_sem_parametro
    with mock.patch(
        "naatividade.management.commands.send_email.send_mass_mail"
    ) as mock_send_mass_mail:
        send_mail_alerta_compra(ativo_magalu.id)
    mock_send_mass_mail.assert_not_called()
