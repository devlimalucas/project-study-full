import tempfile
import pandas as pd
from datetime import date
import pytest
from tests.factories import ProdutoFactory, UsuarioFactory


def test_etl_import_vendas_csv_invalido(client, criar_usuario_admin, autenticar):
    """CSV faltando colunas obrigatórias deve retornar 422"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    df = pd.DataFrame([{"produto_id": 1, "quantidade": 2}])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})

    assert response.status_code == 422
    assert "CSV deve conter colunas" in response.json()["detail"]


def test_etl_import_vendas_estoque_insuficiente(client, criar_usuario_admin, autenticar):
    """Import com quantidade maior que estoque deve retornar 400"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=1).model_dump(), headers=headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=headers).json()

    df = pd.DataFrame([{
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 5,
        "data": str(date.today())
    }])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})

    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]


@pytest.mark.parametrize("role", ["cliente", "vendedor"])
def test_etl_import_vendas_permissao_negada(client, criar_usuario_admin, autenticar, role):
    """Cliente ou vendedor não pode acessar import/export"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers_admin = {"Authorization": f"Bearer {token_admin}"}

    response_user = client.post("/usuarios/", json=UsuarioFactory(role=role).model_dump(), headers=headers_admin)
    usuario = response_user.json()

    token_user = autenticar(client, usuario["email"], "123456")
    headers_user = {"Authorization": f"Bearer {token_user}"}

    response = client.post("/etl/import", headers=headers_user)
    assert response.status_code == 403

    response = client.get("/etl/export", headers=headers_user)
    assert response.status_code == 403


def test_etl_import_vendas_data_invalida(client, criar_usuario_admin, autenticar):
    """CSV com data inválida deve retornar 422"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=10).model_dump(), headers=headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=headers).json()

    df = pd.DataFrame([{
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 1,
        "data": "data_invalida"
    }])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})

    assert response.status_code == 422
    assert "Erro de validação" in response.json()["detail"]


def test_etl_import_vendas_quantidade_invalida(client, criar_usuario_admin, autenticar):
    """CSV com quantidade zero ou negativa deve retornar 422 ou 400"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=10).model_dump(), headers=headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=headers).json()

    # quantidade negativa
    df_neg = pd.DataFrame([{
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": -5,
        "data": str(date.today())
    }])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df_neg.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})
    assert response.status_code in (400, 422)

    # quantidade zero
    df_zero = pd.DataFrame([{
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 0,
        "data": str(date.today())
    }])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df_zero.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})
    assert response.status_code in (400, 422)


def test_etl_import_vendas_formato_invalido(client, criar_usuario_admin, autenticar):
    """Arquivo não-CSV deve retornar 400"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    with tempfile.NamedTemporaryFile(mode="wb+", suffix=".txt") as tmp:
        tmp.write("conteudo invalido".encode())
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.txt", tmp.read(), "text/plain")})

    assert response.status_code == 400
    assert "Formato inválido" in response.json()["detail"]


def test_etl_export_sem_vendas(client, criar_usuario_admin, autenticar):
    """Export sem vendas deve retornar 404"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    response = client.get("/etl/export", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Nenhuma venda encontrada"
