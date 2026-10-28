"""Configurações da aplicação. Valores sensíveis vêm de variáveis de ambiente."""
import os


def _url_banco():
    url = os.environ.get("DATABASE_URL", "sqlite:///cupcakeria.db")
    # Provedores entregam "postgres://" ou "postgresql://". Dizemos explicitamente
    # qual driver usar (psycopg2), pois versões novas do SQLAlchemy mudaram o padrão.
    for prefixo in ("postgres://", "postgresql://"):
        if url.startswith(prefixo):
            return "postgresql+psycopg2://" + url[len(prefixo):]
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-de-desenvolvimento-troque-em-producao")
    SQLALCHEMY_DATABASE_URI = _url_banco()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_SENHA = os.environ.get("ADMIN_SENHA", "admin123")
    CSRF_ATIVO = True
    AUTO_SEED = True  # cadastra cupcakes de exemplo se o banco estiver vazio