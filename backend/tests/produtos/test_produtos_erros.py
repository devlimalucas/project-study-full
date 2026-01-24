import pytest


@pytest.mark.parametrize("payload", [
    {"nome": "P", "preco": 10.0, "estoque": 5},  # nome muito curto
    {"nome": "Produto Inválido", "preco": -1.0, "estoque": 5},  # preço negativo
    {"nome": "Produto Inválido", "preco": 10.0, "estoque": -5},  # estoque negativo
])
def test_criar_produto_invalido(client, criar_usuario_admin, autenticar, payload):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/produtos/", json=payload, headers=headers)
    assert response.status_code == 422


def test_obter_produto_inexistente(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/produtos/9999", headers=headers)
    assert response.status_code == 404


def test_atualizar_produto_inexistente_put(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.put("/produtos/9999", json={"nome": "Novo Nome"}, headers=headers)
    assert response.status_code == 404


def test_atualizar_produto_inexistente_patch(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.patch("/produtos/9999", json={"estoque": 10}, headers=headers)
    assert response.status_code == 404


def test_deletar_produto_inexistente(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/produtos/9999", headers=headers)
    assert response.status_code == 404
