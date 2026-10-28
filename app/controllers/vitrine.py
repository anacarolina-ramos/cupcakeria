"""CONTROLLER da vitrine virtual (US01, US08)."""
from flask import Blueprint, render_template, request

from ..models import Categoria, Cupcake

bp = Blueprint("vitrine", __name__)


@bp.route("/")
def index():
    categoria_id = request.args.get("categoria", type=int)
    consulta = Cupcake.query.filter_by(disponivel=True)
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)
    cupcakes = consulta.order_by(Cupcake.nome).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template("vitrine/index.html", cupcakes=cupcakes,
                           categorias=categorias, categoria_atual=categoria_id)
