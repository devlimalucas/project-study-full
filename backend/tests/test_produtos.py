from schemas.produto import ProdutoCreate


def test_criar_produto(client):
    response = client.post("/produtos/", json={
        "nome": "Produto Teste",
        "preco": 99.99,
        "estoque": 10,
        "descricao": "Produto de teste"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == "Produto Teste"


def test_listar_produtos(client):
    response = client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obter_produto(client):
    novo = client.post("/produtos/", json={
        "nome": "Produto X",
        "preco": 50.00,
        "estoque": 5,
        "descricao": "Teste"
    }).json()
    response = client.get(f"/produtos/{novo['id']}")
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto X"


def test_atualizar_produto(client):
    novo = client.post("/produtos/", json={
        "nome": "Produto Y",
        "preco": 10.00,
        "estoque": 2,
        "descricao": "Teste"
    }).json()
    response = client.put(f"/produtos/{novo['id']}", json={
        "nome": "Produto Y Atualizado",
        "preco": 20.00,
        "estoque": 3,
        "descricao": "Atualizado"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Y Atualizado"


def test_deletar_produto(client):
    novo = client.post("/produtos/", json={
        "nome": "Produto Z",
        "preco": 5.00,
        "estoque": 1,
        "descricao": "Teste"
    }).json()
    response = client.delete(f"/produtos/{novo['id']}")
    assert response.status_code == 204
    assert client.get(f"/produtos/{novo['id']}").status_code == 404


def test_model_dump_produto():
    produto = ProdutoCreate(
        nome="Produto Dump", preco=123.45,
        estoque=7, descricao="Teste model_dump")
    data = produto.model_dump()
    assert data["nome"] == "Produto Dump"
    assert data["preco"] == 123.45
