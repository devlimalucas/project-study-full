import pytest


def test_login_sucesso(client, criar_usuario_admin):
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "senha": "admin123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_acesso_rota_protegida_com_token(client, criar_usuario_admin, autenticar):
    # Faz login para pegar token
    token = autenticar(client, "admin@test.com", "admin123")

    # Usa token para acessar rota protegida
    response = client.get(
        "/usuarios/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
