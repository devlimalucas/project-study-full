from tests.factories import ProdutoFactory
from schemas import ProdutoCreate


def test_criar_produto(client):
    produto = ProdutoFactory()
    response = client.post("/produtos/", json=produto.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == produto.nome


def test_listar_produtos(client):
    produto = ProdutoFactory()
    client.post("/produtos/", json=produto.model_dump())
    response = client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obter_produto(client):
    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump()).json()
    response = client.get(f"/produtos/{novo['id']}")
    assert response.status_code == 200
    assert response.json()["nome"] == produto.nome


def test_atualizar_produto_put(client):
    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump()).json()
    update_data = produto.model_dump()
    update_data["nome"] = "Produto Atualizado"
    response = client.put(f"/produtos/{novo['id']}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Atualizado"


def test_atualizar_produto_patch(client):
    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump()).json()
    patch_data = {"estoque": 99}
    response = client.patch(f"/produtos/{novo['id']}", json=patch_data)
    assert response.status_code == 200
    data = response.json()
    assert data["estoque"] == 99
    assert data["nome"] == produto.nome


def test_deletar_produto(client):
    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump()).json()
    response = client.delete(f"/produtos/{novo['id']}")
    assert response.status_code == 204
    assert client.get(f"/produtos/{novo['id']}").status_code == 404


def test_model_dump_produto():
    produto = ProdutoCreate(
        nome="Produto Dump",
        preco=123.45,
        estoque=7,
        descricao="Teste model_dump"
    )
    data = produto.model_dump()
    assert data["nome"] == "Produto Dump"
    assert data["preco"] == 123.45
