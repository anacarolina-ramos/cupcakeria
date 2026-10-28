"""Regras de validação dos formulários (entrada do usuário)."""
import re
from decimal import Decimal, InvalidOperation

from .models import METODOS_PAGAMENTO

RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
RE_CEP = re.compile(r"^\d{5}-?\d{3}$")
RE_COR = re.compile(r"^#[0-9a-fA-F]{6}$")
PRECO_MAXIMO_CENTAVOS = 1_000_00  # R$ 1.000,00


def parse_preco(texto):
    """Converte '12,50', '12.50' ou 'R$ 1.012,50' em centavos. Retorna None se inválido."""
    if texto is None:
        return None
    t = texto.strip().replace("R$", "").replace(" ", "")
    if not t:
        return None
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        valor = Decimal(t)
    except InvalidOperation:
        return None
    centavos = int((valor * 100).to_integral_value())
    if centavos <= 0 or centavos > PRECO_MAXIMO_CENTAVOS:
        return None
    return centavos


def _limpo(form, campo):
    return (form.get(campo) or "").strip()


def validar_checkout(form):
    """Retorna (dados, erros). 'erros' é um dict campo -> mensagem."""
    dados = {c: _limpo(form, c) for c in (
        "nome", "email", "telefone", "cep", "rua", "numero",
        "complemento", "bairro", "cidade", "metodo")}
    dados["email"] = dados["email"].lower()
    erros = {}

    if len(dados["nome"]) < 3:
        erros["nome"] = "Informe seu nome completo (mínimo 3 letras)."
    if not RE_EMAIL.match(dados["email"]):
        erros["email"] = "Informe um e-mail válido, como nome@exemplo.com."
    if dados["telefone"] and len(re.sub(r"\D", "", dados["telefone"])) not in (10, 11):
        erros["telefone"] = "Telefone deve ter DDD + número (10 ou 11 dígitos)."
    if not RE_CEP.match(dados["cep"]):
        erros["cep"] = "Informe o CEP no formato 00000-000."
    for campo, rotulo in (("rua", "a rua"), ("numero", "o número"),
                          ("bairro", "o bairro"), ("cidade", "a cidade")):
        if not dados[campo]:
            erros[campo] = f"Informe {rotulo}."
    if dados["metodo"] not in METODOS_PAGAMENTO:
        erros["metodo"] = "Escolha uma forma de pagamento: PIX ou cartão."
    return dados, erros


def validar_cupcake(form, categorias_validas):
    """Retorna (dados, erros) para o cadastro/edição de cupcake."""
    dados = {
        "nome": _limpo(form, "nome"),
        "descricao": _limpo(form, "descricao"),
        "preco": _limpo(form, "preco"),
        "cor": _limpo(form, "cor") or "#C2185B",
        "categoria_id": form.get("categoria_id", type=int),
    }
    erros = {}
    if not dados["nome"] or len(dados["nome"]) > 80:
        erros["nome"] = "Informe o nome do sabor (até 80 caracteres)."
    if not dados["descricao"] or len(dados["descricao"]) > 255:
        erros["descricao"] = "Informe a descrição (até 255 caracteres)."
    dados["preco_centavos"] = parse_preco(dados["preco"])
    if dados["preco_centavos"] is None:
        erros["preco"] = "Informe um preço válido entre R$ 0,01 e R$ 1.000,00, como 12,50."
    if not RE_COR.match(dados["cor"]):
        erros["cor"] = "Escolha uma cor válida."
    if dados["categoria_id"] not in categorias_validas:
        erros["categoria_id"] = "Escolha uma categoria."
    return dados, erros
