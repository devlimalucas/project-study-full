import pytest
from tests.factories import UsuarioFactory
from schemas import UsuarioCreate


def test_criar_usuario(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="cliente")
    response = client.post("/usuarios/", json=usuario.model_dump(), headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == usuario.nome
    assert data["email"] == usuario.email
    assert data["role"] == "cliente"


def test_listar_usuarios(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="cliente")
    client.post("/usuarios/", json=usuario.model_dump(), headers=headers)

    response = client.get("/usuarios/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obter_usuario(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="vendedor")
    novo = client.post("/usuarios/", json=usuario.model_dump(), headers=headers).json()

    response = client.get(f"/usuarios/{novo['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == usuario.email


def test_atualizar_usuario_put(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="cliente")
    novo = client.post("/usuarios/", json=usuario.model_dump(), headers=headers).json()

    update_data = usuario.model_dump()
    update_data["nome"] = "Usuário Atualizado"
    update_data["role"] = "vendedor"

    response = client.put(f"/usuarios/{novo['id']}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["nome"] == "Usuário Atualizado"
    assert response.json()["role"] == "vendedor"


def test_atualizar_usuario_patch(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="cliente")
    novo = client.post("/usuarios/", json=usuario.model_dump(), headers=headers).json()

    patch_data = {"nome": "Usuário Parcial"}
    response = client.patch(f"/usuarios/{novo['id']}", json=patch_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Usuário Parcial"
    assert data["email"] == usuario.email
    assert data["role"] == usuario.role


def test_deletar_usuario(client, criar_usuario_admin, autenticar):
    token = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token}"}

    usuario = UsuarioFactory(role="cliente")
    novo = client.post("/usuarios/", json=usuario.model_dump(), headers=headers).json()

    response = client.delete(f"/usuarios/{novo['id']}", headers=headers)
    assert response.status_code == 204
    assert client.get(f"/usuarios/{novo['id']}", headers=headers).status_code == 404


def test_model_dump_usuario():
    usuario = UsuarioCreate(
        nome="Usuário Dump",
        email="dump@teste.com",
        senha="123456",
        role="cliente"
    )
    data = usuario.model_dump()
    assert data["nome"] == "Usuário Dump"
    assert data["email"] == "dump@teste.com"
    assert data["senha"] == "123456"
    assert data["role"] == "cliente"
