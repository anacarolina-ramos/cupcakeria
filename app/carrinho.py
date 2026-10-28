"""Carrinho de compras guardado na sessão do navegador: {id_do_cupcake: quantidade}."""
from flask import session

from .models import Cupcake

MAX_POR_ITEM = 20


def _dados():
    return session.setdefault("carrinho", {})


def adicionar(cupcake_id, quantidade=1):
    carrinho = _dados()
    chave = str(cupcake_id)
    carrinho[chave] = min(carrinho.get(chave, 0) + quantidade, MAX_POR_ITEM)
    session.modified = True


def atualizar(cupcake_id, quantidade):
    """Define a quantidade. Zero ou negativa remove o item."""
    carrinho = _dados()
    chave = str(cupcake_id)
    if chave not in carrinho:
        return
    if quantidade <= 0:
        del carrinho[chave]
    else:
        carrinho[chave] = min(quantidade, MAX_POR_ITEM)
    session.modified = True


def remover(cupcake_id):
    atualizar(cupcake_id, 0)


def limpar():
    session.pop("carrinho", None)


def quantidade_total():
    return sum(session.get("carrinho", {}).values())


def itens_detalhados():
    """Lista de dicts {cupcake, quantidade, subtotal_centavos} dos itens do carrinho."""
    carrinho = session.get("carrinho", {})
    if not carrinho:
        return []
    ids = [int(i) for i in carrinho]
    cupcakes = {c.id: c for c in Cupcake.query.filter(Cupcake.id.in_(ids)).all()}
    itens = []
    for i in ids:
        cupcake = cupcakes.get(i)
        if cupcake is None:
            continue
        qtd = carrinho[str(i)]
        itens.append({"cupcake": cupcake, "quantidade": qtd,
                      "subtotal_centavos": qtd * cupcake.preco_centavos})
    return itens


def total_centavos(itens):
    return sum(i["subtotal_centavos"] for i in itens)
