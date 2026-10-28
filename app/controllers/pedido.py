"""CONTROLLER de checkout, pagamento e acompanhamento (US03, US05, US06, US12)."""
from flask import (Blueprint, abort, flash, redirect, render_template,
                   request, session, url_for)

from .. import carrinho as servico
from ..models import Cliente, Pedido, db
from ..pedidos import criar_pedido
from ..validadores import validar_checkout

bp = Blueprint("pedido", __name__)


def _autorizar(pedido_id):
    autorizados = session.setdefault("pedidos_autorizados", [])
    if pedido_id not in autorizados:
        autorizados.append(pedido_id)
        session.modified = True


@bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    itens = servico.itens_detalhados()
    if not itens:
        flash("Seu carrinho está vazio. Escolha um cupcake para continuar.", "erro")
        return redirect(url_for("vitrine.index"))
    if any(not i["cupcake"].disponivel for i in itens):
        flash("Há um sabor esgotado no carrinho. Remova-o para continuar.", "erro")
        return redirect(url_for("carrinho.ver"))

    total = servico.total_centavos(itens)
    if request.method == "POST":
        dados, erros = validar_checkout(request.form)
        if erros:
            return render_template("pedido/checkout.html", itens=itens, total=total,
                                   dados=dados, erros=erros), 422
        pedido = criar_pedido(dados, itens)
        servico.limpar()
        _autorizar(pedido.id)
        flash("Pagamento aprovado! Seu pedido foi recebido.", "ok")
        return redirect(url_for("pedido.detalhe", pedido_id=pedido.id))

    return render_template("pedido/checkout.html", itens=itens, total=total, dados={}, erros={})


@bp.route("/pedido/<int:pedido_id>")
def detalhe(pedido_id):
    if pedido_id not in session.get("pedidos_autorizados", []):
        flash("Informe o número do pedido e o e-mail para acompanhar.", "erro")
        return redirect(url_for("pedido.acompanhar"))
    pedido = db.session.get(Pedido, pedido_id)
    if pedido is None:
        abort(404)
    return render_template("pedido/detalhe.html", pedido=pedido)


@bp.route("/acompanhar", methods=["GET", "POST"])
def acompanhar():
    if request.method == "POST":
        numero = request.form.get("numero", type=int)
        email = (request.form.get("email") or "").strip().lower()
        pedido = None
        if numero:
            pedido = (Pedido.query.join(Cliente)
                      .filter(Pedido.id == numero, Cliente.email == email).first())
        if pedido is None:
            flash("Não encontramos um pedido com esse número e e-mail.", "erro")
            return render_template("pedido/acompanhar.html"), 404
        _autorizar(pedido.id)
        return redirect(url_for("pedido.detalhe", pedido_id=pedido.id))
    return render_template("pedido/acompanhar.html")
