import pytest
from datetime import date
from tests.factories import ProdutoFactory, UsuarioFactory


def test_criar_venda_estoque_insuficiente(client, criar_usuario_admin, autenticar):
    token_admin = autenticar(client, "admin@test.com", "admin123")
    admin_headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=1).model_dump(), headers=admin_headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=admin_headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=admin_headers).json()

    token_vendedor = autenticar(client, vendedor["email"], "123456")
    vendedor_headers = {"Authorization": f"Bearer {token_vendedor}"}

    payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "quantidade": 5
    }
    response = client.post("/vendas/", json=payload, headers=vendedor_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"


def test_atualizar_venda_estoque_insuficiente(client, criar_usuario_admin, autenticar):
    token_admin = autenticar(client, "admin@test.com", "admin123")
    admin_headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=2).model_dump(), headers=admin_headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=admin_headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=admin_headers).json()

    token_vendedor = autenticar(client, vendedor["email"], "123456")
    vendedor_headers = {"Authorization": f"Bearer {token_vendedor}"}

    venda_payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "quantidade": 1
    }
    venda = client.post("/vendas/", json=venda_payload, headers=vendedor_headers).json()
    assert "id" in venda

    response = client.put(f"/vendas/{venda['id']}", json={"quantidade": 5}, headers=admin_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Estoque insuficiente"


def test_criar_venda_cliente_inexistente(client, criar_usuario_admin, autenticar):
    token_admin = autenticar(client, "admin@test.com", "admin123")
    admin_headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory().model_dump(), headers=admin_headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=admin_headers).json()

    token_vendedor = autenticar(client, vendedor["email"], "123456")
    vendedor_headers = {"Authorization": f"Bearer {token_vendedor}"}

    payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": 9999,  # inexistente
        "quantidade": 1
    }
    response = client.post("/vendas/", json=payload, headers=vendedor_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"


def test_criar_venda_com_role_errada(client, criar_usuario_admin, autenticar):
    token_admin = autenticar(client, "admin@test.com", "admin123")
    admin_headers = {"Authorization": f"Bearer {token_admin}"}

    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=admin_headers).json()
    token_cliente = autenticar(client, cliente["email"], "123456")
    cliente_headers = {"Authorization": f"Bearer {token_cliente}"}

    produto = client.post("/produtos/", json=ProdutoFactory().model_dump(), headers=admin_headers).json()

    payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "quantidade": 1
    }
    response = client.post("/vendas/", json=payload, headers=cliente_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso negado"
