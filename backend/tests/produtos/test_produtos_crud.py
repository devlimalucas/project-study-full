import pytest
from tests.factories import ProdutoFactory
from schemas import ProdutoCreate


def test_criar_produto(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    response = client.post("/produtos/", json=produto.model_dump(), headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == produto.nome


def test_listar_produtos(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    client.post("/produtos/", json=produto.model_dump(), headers=headers)

    response = client.get("/produtos/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obter_produto(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump(), headers=headers).json()

    response = client.get(f"/produtos/{novo['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["nome"] == produto.nome


def test_atualizar_produto_put(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump(), headers=headers).json()

    update_data = produto.model_dump()
    update_data["nome"] = "Produto Atualizado"

    response = client.put(f"/produtos/{novo['id']}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["nome"] == "Produto Atualizado"


def test_atualizar_produto_patch(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump(), headers=headers).json()

    patch_data = {"estoque": 99}
    response = client.patch(f"/produtos/{novo['id']}", json=patch_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["estoque"] == 99
    assert data["nome"] == produto.nome


def test_deletar_produto(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    produto = ProdutoFactory()
    novo = client.post("/produtos/", json=produto.model_dump(), headers=headers).json()

    response = client.delete(f"/produtos/{novo['id']}", headers=headers)
    assert response.status_code == 204
    assert client.get(f"/produtos/{novo['id']}", headers=headers).status_code == 404


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
