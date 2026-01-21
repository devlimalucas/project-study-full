from tests.factories import UsuarioFactory
from schemas import UsuarioCreate

def test_criar_usuario(client):
    usuario = UsuarioFactory(role="cliente")
    response = client.post("/usuarios/", json=usuario.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == usuario.nome
    assert data["email"] == usuario.email
    assert data["role"] == "cliente"

def test_listar_usuarios(client):
    usuario = UsuarioFactory(role="cliente")
    client.post("/usuarios/", json=usuario.model_dump())
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obter_usuario(client):
    usuario = UsuarioFactory(role="vendedor")
    novo = client.post("/usuarios/", json=usuario.model_dump()).json()
    response = client.get(f"/usuarios/{novo['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == usuario.email

def test_atualizar_usuario(client):
    usuario = UsuarioFactory(role="cliente")
    novo = client.post("/usuarios/", json=usuario.model_dump()).json()
    update_data = usuario.model_dump()
    update_data["nome"] = "Usuário Atualizado"
    update_data["role"] = "vendedor"

    response = client.put(f"/usuarios/{novo['id']}", json=update_data)
    assert response.status_code == 200
    assert response.json()["nome"] == "Usuário Atualizado"
    assert response.json()["role"] == "vendedor"

def test_deletar_usuario(client):
    usuario = UsuarioFactory(role="cliente")
    novo = client.post("/usuarios/", json=usuario.model_dump()).json()
    response = client.delete(f"/usuarios/{novo['id']}")
    assert response.status_code == 204
    assert client.get(f"/usuarios/{novo['id']}").status_code == 404

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
