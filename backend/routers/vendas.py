from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Venda, Produto, Usuario
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
    produto = db.query(Produto).filter(Produto.id == venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    cliente = db.query(Usuario).filter(Usuario.id == venda.cliente_id, Usuario.role == "cliente").first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    vendedor = db.query(Usuario).filter(Usuario.id == venda.vendedor_id, Usuario.role == "vendedor").first()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    if venda.quantidade > produto.estoque:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

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

    produto.estoque -= venda.quantidade

    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


@router.put("/{venda_id}", response_model=VendaRead)
@router.patch("/{venda_id}", response_model=VendaRead)
def atualizar_venda(venda_id: int, venda_update: VendaUpdate, db: Session = Depends(get_db)) -> VendaRead:
    db_venda = get_venda_or_404(venda_id, db)
    update_data = venda_update.model_dump(exclude_unset=True)

    if "cliente_id" in update_data:
        cliente = db.query(Usuario).filter(Usuario.id == update_data["cliente_id"], Usuario.role == "cliente").first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if "vendedor_id" in update_data:
        vendedor = db.query(Usuario).filter(Usuario.id == update_data["vendedor_id"], Usuario.role == "vendedor").first()
        if not vendedor:
            raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    nova_quantidade = update_data.get("quantidade", db_venda.quantidade)
    produto = db.query(Produto).filter(Produto.id == db_venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    diferenca = nova_quantidade - db_venda.quantidade
    if diferenca > 0 and diferenca > produto.estoque:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    for key, value in update_data.items():
        setattr(db_venda, key, value)

    produto.estoque -= diferenca
    db_venda.preco_unitario = produto.preco
    db_venda.receita = db_venda.quantidade * db_venda.preco_unitario

    db.commit()
    db.refresh(db_venda)
    return db_venda


@router.delete("/{venda_id}", status_code=204)
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = get_venda_or_404(venda_id, db)

    produto = db.query(Produto).filter(Produto.id == db_venda.produto_id).first()
    if produto:
        produto.estoque += db_venda.quantidade

    db.delete(db_venda)
    db.commit()
    return {"detail": "Venda deletada com sucesso"}
