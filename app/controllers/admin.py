"""CONTROLLER da área do dono da loja e do entregador (US04, US07, US09, US11, US13, US14)."""
import hmac
from functools import wraps

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from sqlalchemy import func

from ..models import STATUS_PEDIDO, Categoria, Cupcake, Pedido, db
from ..validadores import validar_cupcake

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def envelope(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin.login", next=request.path))
        return f(*args, **kwargs)
    return envelope


def _destino_seguro(destino):
    return destino if destino and destino.startswith("/") and not destino.startswith("//") \
        else url_for("admin.pedidos")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        senha = request.form.get("senha", "")
        if hmac.compare_digest(senha.encode(), current_app.config["ADMIN_SENHA"].encode()):
            session["admin"] = True
            return redirect(_destino_seguro(request.args.get("next")))
        flash("Senha incorreta. Tente novamente.", "erro")
        return render_template("admin/login.html"), 401
    return render_template("admin/login.html")


@bp.post("/logout")
def logout():
    session.pop("admin", None)
    flash("Você saiu da área da loja.", "ok")
    return redirect(url_for("vitrine.index"))


@bp.route("/")
@admin_required
def pedidos():
    status = request.args.get("status")
    consulta = Pedido.query.order_by(Pedido.id.desc())
    if status in STATUS_PEDIDO:
        consulta = consulta.filter_by(status=status)
    novos = Pedido.query.filter_by(status="recebido").count()
    return render_template("admin/pedidos.html", pedidos=consulta.all(),
                           status_atual=status, novos=novos)


@bp.post("/pedidos/<int:pedido_id>/status")
@admin_required
def alterar_status(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)
    novo = request.form.get("status")
    if novo not in STATUS_PEDIDO:
        flash("Status inválido.", "erro")
    else:
        pedido.status = novo
        db.session.commit()
        flash(f"Pedido #{pedido.id}: {STATUS_PEDIDO[novo]}.", "ok")
    return redirect(url_for("admin.pedidos"))


@bp.route("/relatorio")
@admin_required
def relatorio():
    """US13: resumo de vendas (pedidos não cancelados)."""
    base = db.session.query(func.count(Pedido.id), func.coalesce(func.sum(Pedido.total_centavos), 0))
    qtd, faturamento = base.filter(Pedido.status != "cancelado").one()
    return render_template("admin/relatorio.html", qtd=qtd, faturamento=faturamento,
                           ticket=(faturamento // qtd if qtd else 0))


@bp.route("/cupcakes")
@admin_required
def cupcakes():
    lista = Cupcake.query.order_by(Cupcake.nome).all()
    return render_template("admin/cupcakes.html", cupcakes=lista)


def _salvar_cupcake(cupcake, titulo):
    categorias = Categoria.query.order_by(Categoria.nome).all()
    if request.method == "POST":
        dados, erros = validar_cupcake(request.form, {c.id for c in categorias})
        if erros:
            return render_template("admin/cupcake_form.html", titulo=titulo,
                                   categorias=categorias, dados=dados, erros=erros), 422
        if cupcake is None:
            cupcake = Cupcake()
            db.session.add(cupcake)
        cupcake.nome = dados["nome"]
        cupcake.descricao = dados["descricao"]
        cupcake.preco_centavos = dados["preco_centavos"]
        cupcake.cor = dados["cor"]
        cupcake.categoria_id = dados["categoria_id"]
        db.session.commit()
        flash(f"Sabor “{cupcake.nome}” salvo.", "ok")
        return redirect(url_for("admin.cupcakes"))
    dados = {}
    if cupcake:
        dados = {"nome": cupcake.nome, "descricao": cupcake.descricao,
                 "preco": f"{cupcake.preco_centavos / 100:.2f}".replace(".", ","),
                 "cor": cupcake.cor, "categoria_id": cupcake.categoria_id}
    return render_template("admin/cupcake_form.html", titulo=titulo,
                           categorias=categorias, dados=dados, erros={})


@bp.route("/cupcakes/novo", methods=["GET", "POST"])
@admin_required
def novo_cupcake():
    return _salvar_cupcake(None, "Novo sabor")


@bp.route("/cupcakes/<int:cupcake_id>/editar", methods=["GET", "POST"])
@admin_required
def editar_cupcake(cupcake_id):
    cupcake = db.get_or_404(Cupcake, cupcake_id)
    return _salvar_cupcake(cupcake, f"Editar {cupcake.nome}")


@bp.post("/cupcakes/<int:cupcake_id>/disponibilidade")
@admin_required
def alternar_disponibilidade(cupcake_id):
    cupcake = db.get_or_404(Cupcake, cupcake_id)
    cupcake.disponivel = not cupcake.disponivel
    db.session.commit()
    estado = "disponível" if cupcake.disponivel else "esgotado"
    flash(f"{cupcake.nome} agora está {estado}.", "ok")
    return redirect(url_for("admin.cupcakes"))
