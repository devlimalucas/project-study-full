import pytest
from datetime import date
from tests.factories import ProdutoFactory, UsuarioFactory


def test_criar_venda_estoque_insuficiente(client):
    produto = client.post("/produtos/", json=ProdutoFactory(estoque=1).model_dump()).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump()).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump()).json()

    response = client.post("/vendas/", json={
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 5
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"


def test_atualizar_venda_estoque_insuficiente(client):
    produto = client.post("/produtos/", json=ProdutoFactory(estoque=2).model_dump()).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump()).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump()).json()

    venda = client.post("/vendas/", json={
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 1
    }).json()

    response = client.put(f"/vendas/{venda['id']}", json={"quantidade": 5})
    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"


def test_criar_venda_cliente_inexistente(client):
    produto = client.post("/produtos/", json=ProdutoFactory().model_dump()).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump()).json()

    payload = {
        "produto_id": produto["id"],
        "cliente_id": 9999,  # inexistente
        "vendedor_id": vendedor["id"],
        "quantidade": 1,
        "data": str(date.today())
    }
    response = client.post("/vendas/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"


def test_criar_venda_vendedor_inexistente(client):
    produto = client.post("/produtos/", json=ProdutoFactory().model_dump()).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump()).json()

    payload = {
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": 9999,  # inexistente
        "quantidade": 1,
        "data": str(date.today())
    }
    response = client.post("/vendas/", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Vendedor não encontrado"


def test_deletar_venda_repoe_estoque(client):
    produto = client.post("/produtos/", json=ProdutoFactory(estoque=5).model_dump()).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump()).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump()).json()

    venda = client.post("/vendas/", json={
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 2
    }).json()

    response = client.delete(f"/vendas/{venda['id']}")
    assert response.status_code == 204

    produto_atualizado = client.get(f"/produtos/{produto['id']}").json()
    assert produto_atualizado["estoque"] == 5
