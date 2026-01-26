from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from infra import get_db
from models import Venda, Produto, Usuario
from schemas import VendaCreate
from schemas import ExportResponse   # <-- import corrigido
from dependencies.auth import get_current_user, role_required
import pandas as pd
import io

router = APIRouter(prefix="/etl", tags=["etl"])

# ---------------------------
# Exportar vendas em CSV
# ---------------------------
@router.get("/export", response_model=ExportResponse, dependencies=[Depends(role_required("admin"))])
def exportar_vendas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    vendas = db.query(Venda).all()
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada")

    df = pd.DataFrame([v.__dict__ for v in vendas])
    if "_sa_instance_state" in df.columns:
        df = df.drop(columns=["_sa_instance_state"])

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    return ExportResponse(filename="vendas_export.csv", content=buffer.getvalue())

# ---------------------------
# Importar vendas via CSV
# ---------------------------
@router.post("/import", dependencies=[Depends(role_required("admin"))])
def importar_vendas(file: UploadFile, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Formato inválido, envie um CSV")

    df = pd.read_csv(file.file)
    required_cols = {"produto_id", "cliente_id", "vendedor_id", "quantidade", "data"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=422, detail=f"CSV deve conter colunas: {required_cols}")

    vendas_importadas = []
    for _, row in df.iterrows():
        try:
            venda_schema = VendaCreate(
                data=row["data"],
                produto_id=row["produto_id"],
                cliente_id=row["cliente_id"],
                quantidade=row["quantidade"],
                vendedor_id=row["vendedor_id"]
            )
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Erro de validação: {e}")

        produto = db.query(Produto).filter(Produto.id == venda_schema.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {venda_schema.produto_id} não encontrado")
        if produto.estoque < venda_schema.quantidade:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para produto {produto.id}")

        cliente = db.query(Usuario).filter(Usuario.id == venda_schema.cliente_id, Usuario.role == "cliente").first()
        vendedor = db.query(Usuario).filter(Usuario.id == venda_schema.vendedor_id, Usuario.role == "vendedor").first()
        if not cliente or not vendedor:
            raise HTTPException(status_code=400, detail="Cliente ou vendedor inválido")

        db_venda = Venda(
            data=venda_schema.data,
            produto_id=venda_schema.produto_id,
            cliente_id=venda_schema.cliente_id,
            vendedor_id=venda_schema.vendedor_id,
            quantidade=venda_schema.quantidade,
            preco_unitario=produto.preco,
            receita=venda_schema.quantidade * produto.preco
        )

        produto.estoque -= venda_schema.quantidade
        db.add(db_venda)
        vendas_importadas.append(db_venda)

    db.commit()
    return {"message": f"{len(vendas_importadas)} vendas importadas com sucesso"}
