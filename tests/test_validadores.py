import pytest
from werkzeug.datastructures import MultiDict

from app.formatacao import brl
from app.validadores import parse_preco, validar_checkout
from tests.conftest import DADOS_CHECKOUT


@pytest.mark.parametrize("texto,esperado", [
    ("12,50", 1250), ("12.50", 1250), ("R$ 1.000,00", 100000), ("9", 900),
    ("", None), ("abc", None), ("0", None), ("-5", None), ("1000,01", None), (None, None),
])
def test_parse_preco(texto, esperado):
    assert parse_preco(texto) == esperado


def test_brl():
    assert brl(1250) == "R$ 12,50"
    assert brl(123456) == "R$ 1.234,56"
    assert brl(0) == "R$ 0,00"


def test_checkout_valido():
    dados, erros = validar_checkout(MultiDict(DADOS_CHECKOUT))
    assert erros == {}
    assert dados["email"] == "maria@exemplo.com"


@pytest.mark.parametrize("campo,valor", [
    ("nome", "Al"), ("email", "sem-arroba"), ("cep", "123"), ("rua", ""),
    ("numero", ""), ("bairro", ""), ("cidade", ""), ("metodo", "boleto"),
    ("telefone", "123"),
])
def test_checkout_campo_invalido(campo, valor):
    form = dict(DADOS_CHECKOUT, **{campo: valor})
    _, erros = validar_checkout(MultiDict(form))
    assert campo in erros
