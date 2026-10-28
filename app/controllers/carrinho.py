"""CONTROLLER do carrinho de compras (US02, US10)."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from .. import carrinho as servico
from ..models import Cupcake, db

bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")


@bp.route("/")
def ver():
    itens = servico.itens_detalhados()
    return render_template("carrinho/ver.html", itens=itens,
                           total=servico.total_centavos(itens),
                           max_item=servico.MAX_POR_ITEM)


@bp.post("/adicionar/<int:cupcake_id>")
def adicionar(cupcake_id):
    cupcake = db.session.get(Cupcake, cupcake_id)
    destino = url_for("vitrine.index", categoria=request.form.get("categoria", type=int))
    if cupcake is None or not cupcake.disponivel:
        flash("Este sabor está esgotado no momento.", "erro")
        return redirect(destino)
    servico.adicionar(cupcake_id)
    flash(f"{cupcake.nome} foi adicionado ao carrinho.", "ok")
    return redirect(destino)


@bp.post("/atualizar/<int:cupcake_id>")
def atualizar(cupcake_id):
    quantidade = request.form.get("quantidade", type=int)
    if quantidade is None:
        flash("Informe a quantidade com um número inteiro.", "erro")
    else:
        servico.atualizar(cupcake_id, quantidade)
        flash("Quantidade atualizada.", "ok")
    return redirect(url_for("carrinho.ver"))


@bp.post("/remover/<int:cupcake_id>")
def remover(cupcake_id):
    servico.remover(cupcake_id)
    flash("Item removido do carrinho.", "ok")
    return redirect(url_for("carrinho.ver"))
