from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Venda, Produto, Usuario
from infra import get_db
from schemas import VendaCreate, VendaRead, VendaUpdate
from dependencies.auth import get_current_user, role_required

router = APIRouter(prefix="/vendas", tags=["vendas"])


def get_venda_or_404(venda_id: int, db: Session) -> Venda:
    venda = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


# Admin vê todas, vendedor só vê as próprias
@router.get("/", response_model=list[VendaRead])
def listar_vendas(db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    if usuario.role == "admin":
        return db.query(Venda).all()
    elif usuario.role == "vendedor":
        return db.query(Venda).filter(Venda.vendedor_id == usuario.id).all()
    raise HTTPException(status_code=403, detail="Acesso negado")


# Admin vê qualquer, vendedor só vê as próprias
@router.get("/{venda_id}", response_model=VendaRead)
def obter_venda(venda_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    venda = get_venda_or_404(venda_id, db)
    if usuario.role == "admin" or (usuario.role == "vendedor" and venda.vendedor_id == usuario.id):
        return venda
    raise HTTPException(status_code=403, detail="Acesso negado")


# Apenas vendedor pode criar vendas
@router.post("/", response_model=VendaRead, status_code=201, dependencies=[Depends(role_required("vendedor"))])
def criar_venda(venda: VendaCreate, db: Session = Depends(get_db), usuario_atual: Usuario = Depends(get_current_user)):
    produto = db.query(Produto).filter(Produto.id == venda.produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    cliente = db.query(Usuario).filter(Usuario.id == venda.cliente_id, Usuario.role == "cliente").first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    if venda.quantidade > produto.estoque:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")

    preco_unitario = produto.preco
    receita = venda.quantidade * preco_unitario

    db_venda = Venda(
        data=venda.data,
        produto_id=venda.produto_id,
        cliente_id=venda.cliente_id,
        vendedor_id=usuario_atual.id,  # usa o vendedor autenticado
        quantidade=venda.quantidade,
        preco_unitario=preco_unitario,
        receita=receita
    )

    produto.estoque -= venda.quantidade

    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    return db_venda


# Apenas admin pode atualizar vendas (PUT e PATCH)
@router.put("/{venda_id}", response_model=VendaRead, dependencies=[Depends(role_required("admin"))])
@router.patch("/{venda_id}", response_model=VendaRead, dependencies=[Depends(role_required("admin"))])
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


# Apenas admin pode deletar vendas
@router.delete("/{venda_id}", status_code=204, dependencies=[Depends(role_required("admin"))])
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    db_venda = get_venda_or_404(venda_id, db)

    produto = db.query(Produto).filter(Produto.id == db_venda.produto_id).first()
    if produto:
        produto.estoque += db_venda.quantidade

    db.delete(db_venda)
    db.commit()
    return  # 204 não retorna corpo
