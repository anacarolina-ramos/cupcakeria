"""Testes do pagamento simulado: código PIX de demonstração e cartão de teste."""
from datetime import date

import pytest
from werkzeug.datastructures import MultiDict

from app.models import Pagamento, Pedido
from app.pagamentos import (CHAVE_PIX_DEMO, luhn_valido, validade_valida,
                            validar_cartao)
from app.validadores import validar_checkout
from tests.conftest import DADOS_CHECKOUT

ANO_FUTURO = f"{(date.today().year + 2) % 100:02d}"
CARTAO_OK = {
    "cartao_numero": "4242 4242 4242 4242",
    "cartao_nome": "Maria Silva",
    "cartao_validade": f"12/{ANO_FUTURO}",
    "cartao_cvv": "123",
}


def _carrinho(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")


# ---------- Funções de validação ----------

@pytest.mark.parametrize("numero, esperado", [
    ("4242 4242 4242 4242", True),
    ("4242-4242-4242-4242", True),
    ("5555 5555 5555 4444", True),
    ("4242 4242 4242 4241", False),   # dígito verificador errado
    ("1234", False),                  # curto demais
    ("abcd efgh ijkl mnop", False),   # não numérico
    ("", False),
    (None, False),
])
def test_luhn(numero, esperado):
    assert luhn_valido(numero) is esperado


def test_validade():
    hoje = date(2026, 11, 5)
    assert validade_valida("11/26", hoje) is True      # o mês atual ainda vale
    assert validade_valida("12/26", hoje) is True
    assert validade_valida("12/2027", hoje) is True
    assert validade_valida("10/26", hoje) is False     # vencido
    assert validade_valida("13/27", hoje) is False     # mês inválido
    assert validade_valida("00/27", hoje) is False
    assert validade_valida("1/27", hoje) is False      # formato errado
    assert validade_valida("12/99", hoje) is False     # distante demais
    assert validade_valida("", hoje) is False


def test_validar_cartao_valido():
    assert validar_cartao(MultiDict(CARTAO_OK)) == {}


@pytest.mark.parametrize("campo, valor", [
    ("cartao_numero", "4242 4242 4242 4241"),
    ("cartao_nome", "Ab"),
    ("cartao_validade", "01/20"),
    ("cartao_cvv", "12"),
    ("cartao_cvv", "12a"),
])
def test_validar_cartao_campo_invalido(campo, valor):
    erros = validar_cartao(MultiDict(dict(CARTAO_OK, **{campo: valor})))
    assert set(erros) == {campo}


# ---------- Integração com a validação do checkout ----------

def test_checkout_pix_nao_exige_dados_de_cartao():
    _, erros = validar_checkout(MultiDict(DADOS_CHECKOUT))
    assert erros == {}


def test_checkout_cartao_exige_dados_de_cartao():
    _, erros = validar_checkout(MultiDict(dict(DADOS_CHECKOUT, metodo="cartao")))
    assert set(erros) == {"cartao_numero", "cartao_nome", "cartao_validade", "cartao_cvv"}


def test_checkout_cartao_valido_nao_devolve_dados_do_cartao():
    dados, erros = validar_checkout(MultiDict(dict(DADOS_CHECKOUT, metodo="cartao", **CARTAO_OK)))
    assert erros == {}
    assert not any(chave.startswith("cartao_") for chave in dados)


# ---------- Rotas ----------

def test_checkout_exibe_codigo_pix_e_campos_do_cartao(client, ids):
    _carrinho(client, ids)
    html = client.get("/checkout").get_data(as_text=True)
    assert CHAVE_PIX_DEMO in html
    assert 'name="cartao_numero"' in html and 'name="cartao_cvv"' in html


def test_pagamento_com_cartao_cria_pedido(app, client, ids):
    _carrinho(client, ids)
    r = client.post("/checkout", data=dict(DADOS_CHECKOUT, metodo="cartao", **CARTAO_OK),
                    follow_redirects=True)
    assert "Cartão: aprovado" in r.get_data(as_text=True)
    with app.app_context():
        assert Pagamento.query.one().metodo == "cartao"


def test_cartao_invalido_nao_cria_pedido_e_nao_devolve_dados(app, client, ids):
    _carrinho(client, ids)
    dados = dict(DADOS_CHECKOUT, metodo="cartao",
                 **dict(CARTAO_OK, cartao_numero="5555 5555 5555 4444", cartao_cvv="12"))
    r = client.post("/checkout", data=dados)
    html = r.get_data(as_text=True)
    assert r.status_code == 422
    assert "3 ou 4 dígitos" in html
    assert "5555" not in html          # o número digitado não volta para a página
    with app.app_context():
        assert Pedido.query.count() == 0


def test_dados_do_cartao_nao_sao_armazenados(app, client, ids):
    _carrinho(client, ids)
    client.post("/checkout", data=dict(DADOS_CHECKOUT, metodo="cartao", **CARTAO_OK))
    with app.app_context():
        colunas = {c.name for c in Pagamento.__table__.columns}
        assert not any(("cartao" in c or "cvv" in c or "numero" in c) for c in colunas)
