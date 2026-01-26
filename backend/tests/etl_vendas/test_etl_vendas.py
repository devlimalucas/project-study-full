import tempfile
import pandas as pd
from datetime import date
from tests.factories import ProdutoFactory, UsuarioFactory


def test_etl_export_vendas(client, criar_usuario_admin, autenticar):
    """Exportar vendas deve retornar CSV com dados"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=10).model_dump(), headers=headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=headers).json()

    token_vendedor = autenticar(client, vendedor["email"], "123456")
    vendedor_headers = {"Authorization": f"Bearer {token_vendedor}"}

    venda_payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "quantidade": 2
    }
    client.post("/vendas/", json=venda_payload, headers=vendedor_headers)

    response = client.get("/etl/export", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "vendas_export.csv"
    assert "produto_id" in data["content"]
    assert str(produto["id"]) in data["content"]
    assert str(cliente["id"]) in data["content"]
    assert str(vendedor["id"]) in data["content"]


def test_etl_import_vendas_valido(client, criar_usuario_admin, autenticar):
    """Importar vendas válidas deve inserir no banco"""
    token_admin = autenticar(client, "admin@test.com", "admin123")
    headers = {"Authorization": f"Bearer {token_admin}"}

    produto = client.post("/produtos/", json=ProdutoFactory(estoque=10).model_dump(), headers=headers).json()
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=headers).json()

    df = pd.DataFrame([{
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "vendedor_id": vendedor["id"],
        "quantidade": 2,
        "data": str(date.today())
    }])
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        tmp.seek(0)
        response = client.post("/etl/import", headers=headers,
                               files={"file": ("vendas.csv", tmp.read(), "text/csv")})

    assert response.status_code == 200
    assert "vendas importadas" in response.json()["message"]

    vendas = client.get("/vendas/", headers=headers).json()
    assert len(vendas) > 0
    assert vendas[0]["produto_id"] == produto["id"]
    assert vendas[0]["cliente_id"] == cliente["id"]
    assert vendas[0]["vendedor_id"] == vendedor["id"]
    assert vendas[0]["quantidade"] == 2
