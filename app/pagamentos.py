"""Pagamento simulado: código PIX de demonstração e validação de cartão de teste.

Nenhum dado de cartão é armazenado nem devolvido ao navegador: os valores são
apenas validados e descartados.
"""
import re
from datetime import date

# Código fictício, que não corresponde a nenhuma conta real.
CHAVE_PIX_DEMO = "DEMO-CUPCAKERIA-PIX-00000012345"
CARTAO_TESTE = "4242 4242 4242 4242"

RE_VALIDADE = re.compile(r"^(\d{2})\s*/\s*(\d{2}|\d{4})$")
RE_CVV = re.compile(r"^[0-9]{3,4}$")
ANOS_MAXIMOS_VALIDADE = 20


def luhn_valido(numero):
    """Confere o dígito verificador (algoritmo de Luhn) de um número de cartão."""
    digitos = re.sub(r"[\s-]", "", numero or "")
    if not re.fullmatch(r"[0-9]+", digitos) or not 13 <= len(digitos) <= 19:
        return False
    soma = 0
    for posicao, digito in enumerate(reversed(digitos)):
        n = int(digito)
        if posicao % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        soma += n
    return soma % 10 == 0


def validade_valida(texto, hoje=None):
    """Aceita MM/AA ou MM/AAAA. O cartão vale até o fim do mês informado."""
    m = RE_VALIDADE.match((texto or "").strip())
    if not m:
        return False
    mes, ano = int(m.group(1)), int(m.group(2))
    if ano < 100:
        ano += 2000
    if not 1 <= mes <= 12:
        return False
    hoje = hoje or date.today()
    if ano > hoje.year + ANOS_MAXIMOS_VALIDADE:
        return False
    return (ano, mes) >= (hoje.year, hoje.month)


def _limpo(form, campo):
    return (form.get(campo) or "").strip()


def validar_cartao(form):
    """Retorna um dict campo -> mensagem de erro. Não devolve os dados digitados."""
    erros = {}
    if not luhn_valido(_limpo(form, "cartao_numero")):
        erros["cartao_numero"] = (
            f"Informe um número de cartão válido. Para testar, use {CARTAO_TESTE}.")
    if not 3 <= len(_limpo(form, "cartao_nome")) <= 60:
        erros["cartao_nome"] = "Informe o nome impresso no cartão (3 a 60 letras)."
    if not validade_valida(_limpo(form, "cartao_validade")):
        erros["cartao_validade"] = "Informe a validade no formato MM/AA, com data futura."
    if not RE_CVV.match(_limpo(form, "cartao_cvv")):
        erros["cartao_cvv"] = "Informe o CVV com 3 ou 4 dígitos."
    return erros
