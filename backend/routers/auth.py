from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security_jwt import verify_password, create_access_token
from infra import get_db
from models import Usuario
from schemas.auth import UsuarioLogin, Token

router = APIRouter(prefix="/auth", tags=["autenticacao"])


@router.post("/login", response_model=Token)
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario or not verify_password(usuario.senha, db_usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": str(db_usuario.id), "role": db_usuario.role})
    return {"access_token": token, "token_type": "bearer"}
