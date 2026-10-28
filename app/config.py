"""Configurações da aplicação. Valores sensíveis vêm de variáveis de ambiente."""
import os


def _url_banco():
    url = os.environ.get("DATABASE_URL", "sqlite:///cupcakeria.db")
    # Alguns provedores entregam "postgres://", mas o SQLAlchemy exige "postgresql://"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-troque-em-producao")
    SQLALCHEMY_DATABASE_URI = _url_banco()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SENHA = os.environ.get("ADMIN_SENHA", "admin123")
    CSRF_ATIVO = True
    AUTO_SEED = True  # cadastra cupcakes de exemplo se o banco estiver vazio
