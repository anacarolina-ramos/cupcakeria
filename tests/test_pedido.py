from app.models import Cliente, ItemPedido, Pagamento, Pedido, db
from tests.conftest import DADOS_CHECKOUT


def _carrinho_com(client, ids, nome="Baunilha", vezes=2):
    for _ in range(vezes):
        client.post(f"/carrinho/adicionar/{ids[nome]}")


def test_checkout_com_carrinho_vazio_redireciona(client):
    r = client.get("/checkout", follow_redirects=True)
    assert "carrinho está vazio" in r.get_data(as_text=True)


def test_checkout_formulario_invalido_nao_cria_pedido(app, client, ids):
    _carrinho_com(client, ids)
    r = client.post("/checkout", data=dict(DADOS_CHECKOUT, email="x", cep="1"))
    assert r.status_code == 422
    html = r.get_data(as_text=True)
    assert "e-mail válido" in html and "CEP" in html
    with app.app_context():
        assert Pedido.query.count() == 0


def test_checkout_preserva_dados_digitados_no_erro(client, ids):
    _carrinho_com(client, ids)
    r = client.post("/checkout", data=dict(DADOS_CHECKOUT, email="x"))
    assert "Maria Silva" in r.get_data(as_text=True)


def test_checkout_sucesso(app, client, ids):
    _carrinho_com(client, ids)
    r = client.post("/checkout", data=DADOS_CHECKOUT, follow_redirects=True)
    html = r.get_data(as_text=True)
    assert r.status_code == 200
    assert "Pedido #1" in html and "R$ 18,00" in html and "Pedido recebido" in html
    with app.app_context():
        pedido = db.session.get(Pedido, 1)
        assert pedido.total_centavos == 1800
        assert pedido.status == "recebido"
        assert ItemPedido.query.count() == 1
        assert Pagamento.query.one().metodo == "pix"
    assert "carrinho está vazio" in client.get("/carrinho/").get_data(as_text=True)


def test_cliente_recorrente_nao_duplica(app, client, ids):
    for _ in range(2):
        _carrinho_com(client, ids, vezes=1)
        client.post("/checkout", data=DADOS_CHECKOUT)
    with app.app_context():
        assert Cliente.query.count() == 1
        assert Pedido.query.count() == 2


def test_preco_do_item_e_congelado_no_pedido(app, client, ids):
    _carrinho_com(client, ids, vezes=1)
    client.post("/checkout", data=DADOS_CHECKOUT)
    with app.app_context():
        from app.models import Cupcake
        db.session.get(Cupcake, ids["Baunilha"]).preco_centavos = 5000
        db.session.commit()
        assert ItemPedido.query.one().preco_unitario_centavos == 900


def test_checkout_bloqueia_item_que_esgotou(client, ids, app):
    _carrinho_com(client, ids, vezes=1)
    with app.app_context():
        from app.models import Cupcake
        db.session.get(Cupcake, ids["Baunilha"]).disponivel = False
        db.session.commit()
    r = client.get("/checkout", follow_redirects=True)
    assert "esgotado" in r.get_data(as_text=True)


def test_detalhe_exige_autorizacao(client):
    r = client.get("/pedido/1", follow_redirects=True)
    assert "número do pedido" in r.get_data(as_text=True)


def test_acompanhar_com_email_correto(app, client, ids):
    _carrinho_com(client, ids)
    client.post("/checkout", data=DADOS_CHECKOUT)
    outro = app.test_client()
    r = outro.post("/acompanhar", data={"numero": "1", "email": "MARIA@exemplo.com"},
                   follow_redirects=True)
    assert "Pedido #1" in r.get_data(as_text=True)


def test_acompanhar_com_email_errado(app, client, ids):
    _carrinho_com(client, ids)
    client.post("/checkout", data=DADOS_CHECKOUT)
    r = app.test_client().post("/acompanhar", data={"numero": "1", "email": "outra@x.com"})
    assert r.status_code == 404
    assert "Não encontramos" in r.get_data(as_text=True)
