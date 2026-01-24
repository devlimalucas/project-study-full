from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.security_jwt import decode_access_token
from infra import get_db
from models import Usuario

# Usa sempre o mesmo tokenUrl com barra inicial
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    usuario = db.query(Usuario).filter(Usuario.id == int(payload["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario

def role_required(role: str):
    def wrapper(usuario: Usuario = Depends(get_current_user)):
        if usuario.role != role:
            raise HTTPException(status_code=403, detail="Acesso negado")
        return usuario
    return wrapper
