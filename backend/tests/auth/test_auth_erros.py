import pytest


def test_login_falha_senha_errada(client, criar_usuario_admin):
    # tenta logar com senha incorreta
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "senha": "senha_errada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_login_falha_usuario_inexistente(client):
    # tenta logar com usuário que não existe
    response = client.post("/auth/login", json={
        "email": "naoexiste@test.com",
        "senha": "qualquer"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas"


def test_acesso_rota_protegida_sem_token(client):
    # acessa rota protegida sem enviar token
    response = client.get("/usuarios/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
