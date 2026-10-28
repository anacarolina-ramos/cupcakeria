def test_vitrine_lista_apenas_disponiveis(client):
    html = client.get("/").get_data(as_text=True)
    assert "Baunilha" in html and "Red Velvet" in html
    assert "Esgotado" not in html


def test_vitrine_filtra_por_categoria(client, ids):
    html = client.get(f"/?categoria={ids['cat_Veganos']}").get_data(as_text=True)
    assert "Red Velvet" in html and "Baunilha" not in html


def test_adicionar_ao_carrinho(client, ids):
    r = client.post(f"/carrinho/adicionar/{ids['Baunilha']}", follow_redirects=True)
    assert "foi adicionado ao carrinho" in r.get_data(as_text=True)
    html = client.get("/carrinho/").get_data(as_text=True)
    assert "Baunilha" in html and "R$ 9,00" in html


def test_adicionar_duas_vezes_soma_quantidade(client, ids):
    for _ in range(2):
        client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    assert "R$ 18,00" in client.get("/carrinho/").get_data(as_text=True)


def test_nao_adiciona_esgotado(client, ids):
    r = client.post(f"/carrinho/adicionar/{ids['Esgotado']}", follow_redirects=True)
    assert "esgotado" in r.get_data(as_text=True)
    assert "vazio" in client.get("/carrinho/").get_data(as_text=True)


def test_nao_adiciona_inexistente(client):
    r = client.post("/carrinho/adicionar/9999", follow_redirects=True)
    assert "esgotado" in r.get_data(as_text=True)


def test_editar_quantidade(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    client.post(f"/carrinho/atualizar/{ids['Baunilha']}", data={"quantidade": "3"})
    assert "R$ 27,00" in client.get("/carrinho/").get_data(as_text=True)


def test_quantidade_zero_remove(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    client.post(f"/carrinho/atualizar/{ids['Baunilha']}", data={"quantidade": "0"})
    assert "Seu carrinho está vazio" in client.get("/carrinho/").get_data(as_text=True)


def test_quantidade_invalida_e_tratada(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    r = client.post(f"/carrinho/atualizar/{ids['Baunilha']}", data={"quantidade": "abc"},
                    follow_redirects=True)
    assert "número inteiro" in r.get_data(as_text=True)


def test_quantidade_limitada_ao_maximo(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    client.post(f"/carrinho/atualizar/{ids['Baunilha']}", data={"quantidade": "999"})
    assert "R$ 180,00" in client.get("/carrinho/").get_data(as_text=True)  # 20 x 9,00


def test_remover_item(client, ids):
    client.post(f"/carrinho/adicionar/{ids['Baunilha']}")
    client.post(f"/carrinho/remover/{ids['Baunilha']}")
    assert "Seu carrinho está vazio" in client.get("/carrinho/").get_data(as_text=True)
