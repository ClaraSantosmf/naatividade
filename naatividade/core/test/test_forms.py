import pytest
from django.test import Client
from naatividade.core.models import Ativo


def test_status_code(client: Client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_lista_ativos(db, client: Client):
    resp = client.get("/")
    ativo = Ativo(nome="Petrobras", symbol="Petra")
    ativo.save()
    assert resp.status_code == 200
