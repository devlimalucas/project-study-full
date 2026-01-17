from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.produto import Produto
from infra.deps import get_db
from schemas.produto import ProdutoCreate, ProdutoRead, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["produtos"])


def get_produto_or_404(produto_id: int, db: Session) -> Produto:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.get("/", response_model=list[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db)) -> list[ProdutoRead]:
    return db.query(Produto).all()


@router.get("/{produto_id}", response_model=ProdutoRead)
def obter_produto(produto_id: int, db: Session
                  = Depends(get_db)) -> ProdutoRead:
    return get_produto_or_404(produto_id, db)


@router.post("/", response_model=ProdutoRead, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session
                  = Depends(get_db)) -> ProdutoRead:
    db_produto = Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.put("/{produto_id}", response_model=ProdutoRead)
def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session =
                      Depends(get_db)) -> ProdutoRead:
    db_produto = get_produto_or_404(produto_id, db)

    update_data = produto.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_produto, key, value)

    db.commit()
    db.refresh(db_produto)
    return db_produto


@router.delete("/{produto_id}", status_code=204)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = get_produto_or_404(produto_id, db)
    db.delete(db_produto)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}
