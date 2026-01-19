from schemas import UsuarioCreate

def test_criar_usuario(client):
    response = client.post("/usuarios/", json={
        "nome": "Usuário Teste",
        "email": "teste@teste.com",
        "senha": "123456",
        "role": "cliente"
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["nome"] == "Usuário Teste"
    assert data["email"] == "teste@teste.com"
    assert data["role"] == "cliente"


def test_listar_usuarios(client):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_obter_usuario(client):
    novo = client.post("/usuarios/", json={
        "nome": "Usuário X",
        "email": "x@teste.com",
        "senha": "123456",
        "role": "vendedor"
    }).json()
    response = client.get(f"/usuarios/{novo['id']}")
    assert response.status_code == 200
    assert response.json()["email"] == "x@teste.com"


def test_atualizar_usuario(client):
    novo = client.post("/usuarios/", json={
        "nome": "Usuário Y",
        "email": "y@teste.com",
        "senha": "123456",
        "role": "cliente"
    }).json()
    response = client.put(f"/usuarios/{novo['id']}", json={
        "nome": "Usuário Y Atualizado",
        "role": "vendedor"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Usuário Y Atualizado"
    assert response.json()["role"] == "vendedor"


def test_deletar_usuario(client):
    novo = client.post("/usuarios/", json={
        "nome": "Usuário Z",
        "email": "z@teste.com",
        "senha": "123456",
        "role": "cliente"
    }).json()
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
