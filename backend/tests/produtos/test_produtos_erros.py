import pytest

@pytest.mark.parametrize("payload", [
    {"nome": "P", "preco": 10.0, "estoque": 5},  # nome muito curto
    {"nome": "Produto Inválido", "preco": -1.0, "estoque": 5},  # preço negativo
    {"nome": "Produto Inválido", "preco": 10.0, "estoque": -5},  # estoque negativo
])
def test_criar_produto_invalido(client, payload):
    response = client.post("/produtos/", json=payload)
    assert response.status_code == 422


def test_obter_produto_inexistente(client):
    response = client.get("/produtos/9999")
    assert response.status_code == 404


def test_atualizar_produto_inexistente_put(client):
    response = client.put("/produtos/9999", json={"nome": "Novo Nome"})
    assert response.status_code == 404


def test_atualizar_produto_inexistente_patch(client):
    response = client.patch("/produtos/9999", json={"estoque": 10})
    assert response.status_code == 404


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == 404
