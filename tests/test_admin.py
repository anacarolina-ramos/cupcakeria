from app.models import Cupcake, Pedido, db
from tests.conftest import DADOS_CHECKOUT


def test_area_admin_exige_login(client):
    r = client.get("/admin/")
    assert r.status_code == 302 and "/admin/login" in r.headers["Location"]


def test_login_senha_errada(client):
    r = client.post("/admin/login", data={"senha": "errada"})
    assert r.status_code == 401
    assert "Senha incorreta" in r.get_data(as_text=True)


def test_login_correto(client):
    r = client.post("/admin/login", data={"senha": "senha-teste"})
    assert r.status_code == 302


def test_login_nao_redireciona_para_site_externo(client):
    r = client.post("/admin/login?next=//malicioso.com", data={"senha": "senha-teste"})
    assert "malicioso" not in r.headers["Location"]


def test_cadastrar_cupcake(app, admin, ids):
    r = admin.post("/admin/cupcakes/novo", data={
        "nome": "Café", "descricao": "Com café", "preco": "13,90",
        "cor": "#8B5A2B", "categoria_id": ids["cat_Clássicos"]}, follow_redirects=True)
    assert "salvo" in r.get_data(as_text=True)
    with app.app_context():
        assert Cupcake.query.filter_by(nome="Café").one().preco_centavos == 1390


def test_cadastrar_cupcake_preco_invalido(app, admin, ids):
    r = admin.post("/admin/cupcakes/novo", data={
        "nome": "Café", "descricao": "x", "preco": "abc",
        "cor": "#8B5A2B", "categoria_id": ids["cat_Clássicos"]})
    assert r.status_code == 422 and "preço válido" in r.get_data(as_text=True)
    with app.app_context():
        assert Cupcake.query.filter_by(nome="Café").count() == 0


def test_editar_cupcake(app, admin, ids):
    admin.post(f"/admin/cupcakes/{ids['Baunilha']}/editar", data={
        "nome": "Baunilha Plus", "descricao": "Nova", "preco": "10,00",
        "cor": "#FFFFFF", "categoria_id": ids["cat_Clássicos"]})
    with app.app_context():
        assert db.session.get(Cupcake, ids["Baunilha"]).nome == "Baunilha Plus"


def test_marcar_esgotado_remove_da_vitrine(admin, client, ids):
    admin.post(f"/admin/cupcakes/{ids['Baunilha']}/disponibilidade", follow_redirects=True)
    assert "Baunilha" not in client.get("/").get_data(as_text=True)


def test_alterar_status_do_pedido(app, admin, ids):
    admin.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    admin.post("/checkout", data=DADOS_CHECKOUT)
    admin.post("/admin/pedidos/1/status", data={"status": "entregue"})
    with app.app_context():
        assert db.session.get(Pedido, 1).status == "entregue"


def test_status_invalido_e_rejeitado(app, admin, ids):
    admin.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    admin.post("/checkout", data=DADOS_CHECKOUT)
    r = admin.post("/admin/pedidos/1/status", data={"status": "voando"}, follow_redirects=True)
    assert "Status inválido" in r.get_data(as_text=True)


def test_relatorio(admin, ids):
    admin.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    admin.post("/checkout", data=DADOS_CHECKOUT)
    html = admin.get("/admin/relatorio").get_data(as_text=True)
    assert "R$ 9,00" in html


def test_alerta_de_novos_pedidos(admin, ids):
    admin.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    admin.post("/checkout", data=DADOS_CHECKOUT)
    assert "1 pedido novo" in admin.get("/admin/").get_data(as_text=True)


def test_csrf_bloqueia_post_sem_token(app):
    app.config["CSRF_ATIVO"] = True
    r = app.test_client().post("/carrinho/adicionar/1")
    assert r.status_code == 400
