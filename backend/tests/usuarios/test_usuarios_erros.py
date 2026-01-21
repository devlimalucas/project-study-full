import pytest

@pytest.mark.parametrize("payload", [
    {"nome": "Usuário Teste", "email": "email_invalido", "senha": "123456", "role": "cliente"},
    {"nome": "Usuário Teste", "email": "teste@", "senha": "123456", "role": "cliente"},
    {"nome": "Usuário Teste", "email": "teste.com", "senha": "123456", "role": "cliente"},
])
def test_criar_usuario_email_invalido(client, payload):
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 422


def test_criar_usuario_senha_curta(client):
    payload = {"nome": "Usuário Teste", "email": "teste@teste.com", "senha": "123", "role": "cliente"}
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == 422


def test_obter_usuario_inexistente(client):
    response = client.get("/usuarios/9999")
    assert response.status_code == 404


def test_atualizar_usuario_inexistente_put(client):
    response = client.put("/usuarios/9999", json={"nome": "Novo Nome"})
    assert response.status_code == 404


def test_atualizar_usuario_inexistente_patch(client):
    response = client.patch("/usuarios/9999", json={"nome": "Nome Parcial"})
    assert response.status_code == 404


def test_deletar_usuario_inexistente(client):
    response = client.delete("/usuarios/9999")
    assert response.status_code == 404
