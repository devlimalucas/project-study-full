from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Venda, Produto
from infra import get_db
from schemas import VendaCreate, VendaRead, VendaUpdate

router = APIRouter(prefix="/vendas", tags=["vendas"])


def get_venda_or_404(venda_id: int, db: Session) -> Venda:
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


@router.get("/", response_model=list[VendaRead])
def listar_vendas(db: Session = Depends(get_db)) -> list[VendaRead]:
    return db.query(Venda).all()


@router.get("/{venda_id}", response_model=VendaRead)
def obter_venda(venda_id: int, db: Session = Depends(get_db)) -> VendaRead:
    return get_venda_or_404(venda_id, db)


@router.post("/", response_model=VendaRead, status_code=201)
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db)) -> VendaRead:
    # buscar o produto correto
    produto = db.query(Produto).filter(Produto.id == venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    preco_unitario = produto.preco
    receita = venda.quantidade * preco_unitario

    db_venda = Venda(
        data=venda.data,
        produto_id=venda.produto_id,
        cliente_id=venda.cliente_id,
        vendedor_id=venda.vendedor_id,
        quantidade=venda.quantidade,
        preco_unitario=preco_unitario,
        receita=receita
    )
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


@router.put("/{venda_id}", response_model=VendaRead)
@router.patch("/{venda_id}", response_model=VendaRead)
def atualizar_venda(venda_id: int, venda_update: VendaUpdate, db: Session = Depends(get_db)) -> VendaRead:
    db_venda = get_venda_or_404(venda_id, db)

    update_data = venda_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_venda, key, value)

    # buscar o produto correto e recalcular receita
    produto = db.query(Produto).filter(Produto.id == db_venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db_venda.preco_unitario = produto.preco
    db_venda.receita = db_venda.quantidade * db_venda.preco_unitario

    db.commit()
    db.refresh(db_venda)
    return db_venda


@router.delete("/{venda_id}", status_code=204)
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = get_venda_or_404(venda_id, db)
    db.delete(db_venda)
    db.commit()
    return {"detail": "Venda deletada com sucesso"}
