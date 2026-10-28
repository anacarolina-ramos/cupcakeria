import pytest

from app import create_app
from app.models import Categoria, Cupcake, db


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "CSRF_ATIVO": False,
        "AUTO_SEED": False,
        "ADMIN_SENHA": "senha-teste",
        "SECRET_KEY": "teste",
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
        classicos = Categoria(nome="Clássicos")
        veganos = Categoria(nome="Veganos")
        db.session.add_all([
            Cupcake(nome="Baunilha", descricao="Clássico", preco_centavos=900, categoria=classicos),
            Cupcake(nome="Red Velvet", descricao="Vegano", preco_centavos=1400, categoria=veganos),
            Cupcake(nome="Esgotado", descricao="Acabou", preco_centavos=1000,
                    categoria=classicos, disponivel=False),
        ])
        db.session.commit()
        yield app
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def ids(app):
    with app.app_context():
        return {c.nome: c.id for c in Cupcake.query.all()} | \
               {"cat_" + c.nome: c.id for c in Categoria.query.all()}


@pytest.fixture()
def admin(client):
    client.post("/admin/login", data={"senha": "senha-teste"})
    return client


DADOS_CHECKOUT = {
    "nome": "Maria Silva", "email": "maria@exemplo.com", "telefone": "(11) 91234-5678",
    "cep": "09010-100", "rua": "Rua das Flores", "numero": "10", "complemento": "",
    "bairro": "Centro", "cidade": "Santo André", "metodo": "pix",
}
