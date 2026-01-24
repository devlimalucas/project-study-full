import pytest
from datetime import date
from tests.factories import ProdutoFactory, UsuarioFactory


def test_criar_venda_e_deletar_repoe_estoque(client, criar_usuario_admin, autenticar):
    # autentica admin
    token_admin = autenticar(client, "admin@test.com", "admin123")
    admin_headers = {"Authorization": f"Bearer {token_admin}"}

    # admin cria produto
    produto = client.post("/produtos/", json=ProdutoFactory(estoque=5).model_dump(), headers=admin_headers).json()

    # cria cliente e vendedor via admin
    cliente = client.post("/usuarios/", json=UsuarioFactory(role="cliente").model_dump(), headers=admin_headers).json()
    vendedor = client.post("/usuarios/", json=UsuarioFactory(role="vendedor").model_dump(), headers=admin_headers).json()

    # autentica vendedor
    token_vendedor = autenticar(client, vendedor["email"], "123456")
    vendedor_headers = {"Authorization": f"Bearer {token_vendedor}"}

    # cria venda (sem vendedor_id no payload!)
    venda_payload = {
        "data": str(date.today()),
        "produto_id": produto["id"],
        "cliente_id": cliente["id"],
        "quantidade": 2
    }
    venda = client.post("/vendas/", json=venda_payload, headers=vendedor_headers).json()
    assert "id" in venda

    # deleta venda (admin)
    response = client.delete(f"/vendas/{venda['id']}", headers=admin_headers)
    assert response.status_code == 204

    # estoque deve ser reposto
    produto_atualizado = client.get(f"/produtos/{produto['id']}", headers=admin_headers).json()
    assert produto_atualizado["estoque"] == 5
