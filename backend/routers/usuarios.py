from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Usuario
from infra import get_db
from schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate
from core.security_jwt import get_password_hash
from dependencies.auth import get_current_user, role_required

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def get_usuario_or_404(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario


# Apenas admin pode listar todos os usuários
@router.get("/", response_model=list[UsuarioRead], dependencies=[Depends(role_required("admin"))])
def listar_usuarios(db: Session = Depends(get_db)) -> list[UsuarioRead]:
    return db.query(Usuario).all()


# Admin pode ver qualquer usuário, cliente só o próprio perfil
@router.get("/{usuario_id}", response_model=UsuarioRead)
def obter_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
) -> UsuarioRead:
    if usuario_atual.role != "admin" and usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return get_usuario_or_404(usuario_id, db)


# Apenas admin pode criar usuários
@router.post("/", response_model=UsuarioRead, status_code=201, dependencies=[Depends(role_required("admin"))])
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)) -> UsuarioRead:
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=get_password_hash(usuario.senha),  # aplica hash
        role=usuario.role
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Admin pode atualizar qualquer usuário, cliente só o próprio
@router.put("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
) -> UsuarioRead:
    if usuario_atual.role != "admin" and usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    db_usuario = get_usuario_or_404(usuario_id, db)
    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "senha":
            setattr(db_usuario, "senha_hash", get_password_hash(value))
        else:
            setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.patch("/{usuario_id}", response_model=UsuarioRead)
def atualizar_usuario_parcial(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_current_user)
) -> UsuarioRead:
    if usuario_atual.role != "admin" and usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    db_usuario = get_usuario_or_404(usuario_id, db)
    update_data = usuario.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "senha":
            setattr(db_usuario, "senha_hash", get_password_hash(value))
        else:
            setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


# Apenas admin pode deletar usuários
@router.delete("/{usuario_id}", status_code=204, dependencies=[Depends(role_required("admin"))])
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario_or_404(usuario_id, db)
    db.delete(db_usuario)
    db.commit()
    return {"detail": "Usuário deletado com sucesso"}
