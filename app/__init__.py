"""Fábrica da aplicação Flask (Cupcakeria)."""
import secrets

import click
from flask import Flask, abort, render_template, request, session

from .config import Config
from .formatacao import brl
from .models import STATUS_PEDIDO, db


def gerar_csrf():
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_hex(16)
    return session["_csrf"]


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    app.jinja_env.filters["brl"] = brl

    from .controllers import admin, carrinho, pedido, vitrine
    for modulo in (vitrine, carrinho, pedido, admin):
        app.register_blueprint(modulo.bp)

    @app.context_processor
    def contexto_global():
        from .carrinho import quantidade_total
        return {
            "csrf_token": gerar_csrf,
            "qtd_carrinho": quantidade_total(),
            "admin_logado": session.get("admin", False),
            "STATUS_PEDIDO": STATUS_PEDIDO,
        }

    @app.before_request
    def proteger_csrf():
        if app.config["CSRF_ATIVO"] and request.method == "POST":
            if not session.get("_csrf") or session["_csrf"] != request.form.get("_csrf"):
                abort(400)

    @app.errorhandler(400)
    def erro_400(_):
        return render_template("erro.html", titulo="Requisição inválida",
                               mensagem="Sua sessão expirou ou o formulário é inválido. "
                                        "Volte e tente novamente."), 400

    @app.errorhandler(404)
    def erro_404(_):
        return render_template("erro.html", titulo="Página não encontrada",
                               mensagem="Não encontramos o que você procurou."), 404

    @app.errorhandler(500)
    def erro_500(_):
        db.session.rollback()
        return render_template("erro.html", titulo="Algo deu errado",
                               mensagem="Tivemos um problema. Tente novamente em instantes."), 500

    with app.app_context():
        db.create_all()
        if app.config["AUTO_SEED"]:
            from .seed import seed_se_vazio
            seed_se_vazio()

    @app.cli.command("seed")
    def seed_cmd():
        """Cadastra os cupcakes de exemplo (se o banco estiver vazio)."""
        from .seed import seed_se_vazio
        click.echo("Dados cadastrados." if seed_se_vazio() else "Banco já possui dados.")

    return app
