from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from infra import get_db
from schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_usuario_or_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)) -> list[UsuarioRead]:
    return db.query(Usuario).all()


@router.get("/{usuario_id}", response_model=UsuarioRead)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)) -> UsuarioRead:
    return get_usuario_or_404(usuario_id, db)


@router.post("/", response_model=UsuarioRead, status_code=201)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)) -> UsuarioRead:
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=usuario.senha,  # depois vamos aplicar hash no Dia 5
        role=usuario.role
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)) -> UsuarioRead:
    db_usuario = get_usuario_or_404(usuario_id, db)

    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "senha":
            setattr(db_usuario, "senha_hash", value)
        else:
            setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}", status_code=204)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario_or_404(usuario_id, db)
    db.delete(db_usuario)
    db.commit()
    return {"detail": "Usuário deletado com sucesso"}
