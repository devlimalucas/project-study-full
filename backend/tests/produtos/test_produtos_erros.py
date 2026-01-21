import pytest

@pytest.mark.parametrize("payload", [
    {"nome": "ab", "preco": 10.0, "estoque": 5, "descricao": "Nome curto"},
    {"nome": "Produto OK", "preco": -10, "estoque": 5, "descricao": "Preço negativo"},
    {"nome": "Produto OK", "preco": 10.0, "estoque": -1, "descricao": "Estoque negativo"},
])
def test_criar_produto_invalido(client, payload):
    response = client.post("/produtos/", json=payload)
    assert response.status_code == 422


def test_obter_produto_inexistente(client):
    response = client.get("/produtos/9999")
    assert response.status_code == 404


def test_atualizar_produto_inexistente(client):
    response = client.put("/produtos/9999", json={"nome": "Novo Nome"})
    assert response.status_code == 404


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/9999")
    assert response.status_code == 404
