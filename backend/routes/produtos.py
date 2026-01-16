from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.produto import Produto
from infra.deps import get_db
from schemas.produto import ProdutoCreate, ProdutoRead

router = APIRouter(prefix="/produtos", tags=["produtos"])


@router.get("/", response_model=list[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@router.post("/", response_model=ProdutoRead)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Produto(
        nome=produto.nome,
        preco=produto.preco,
        estoque=produto.estoque,
        descricao=produto.descricao
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto
