from sqlalchemy.orm import Session
from infra import SessionLocal
from core.security_jwt import get_password_hash
from models import Produto, Usuario

# Dados iniciais centralizados
PRODUTOS_INICIAIS = [
    {"nome": "Notebook Dell", "preco": 3500.00, "estoque": 10, "descricao": "Notebook para uso profissional"},
    {"nome": "Mouse USB", "preco": 100.00, "estoque": 50, "descricao": "Mouse simples com fio"},
    {"nome": "Monitor Full HD", "preco": 800.00, "estoque": 5, "descricao": "Monitor 24 polegadas"},
]

USUARIOS_INICIAIS = [
    {"nome": "Admin", "email": "admin@teste.com", "senha": "admin123", "role": "admin"},
    {"nome": "Cliente Inicial", "email": "cliente@teste.com", "senha": "123456", "role": "cliente"},
    {"nome": "Vendedor Inicial", "email": "vendedor@teste.com", "senha": "123456", "role": "vendedor"},
]


def seed_produtos(db: Session):
    if not db.query(Produto).first():
        produtos = [Produto(**p) for p in PRODUTOS_INICIAIS]
        db.bulk_save_objects(produtos)
        print(f"🌱 {len(produtos)} produtos iniciais inseridos")
    else:
        print("ℹ️ Produtos já existentes, nenhum inserido.")


def seed_usuarios(db: Session):
    count = 0
    for u in USUARIOS_INICIAIS:
        if not db.query(Usuario).filter_by(email=u["email"]).first():
            senha_truncada = u["senha"][:72]  # garante compatibilidade com bcrypt
            usuario = Usuario(
                nome=u["nome"],
                email=u["email"],
                senha_hash=get_password_hash(senha_truncada),
                role=u["role"]
            )
            db.add(usuario)
            count += 1
            print(f"🌱 Usuário {u['role']} ({u['email']}) inserido")
        else:
            print(f"ℹ️ Usuário {u['email']} já existe, não inserido.")
    if count:
        print(f"🌱 {count} usuários iniciais inseridos")
    else:
        print("ℹ️ Nenhum usuário novo inserido.")


def run():
    with SessionLocal() as db:
        print("🚀 Iniciando processo de seed...")
        seed_produtos(db)
        seed_usuarios(db)
        db.commit()
        print("✅ Seed concluído com sucesso.")


if __name__ == "__main__":
    run()
