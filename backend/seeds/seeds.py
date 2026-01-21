from sqlalchemy.orm import Session
from infra import SessionLocal, get_password_hash
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


def seed_usuarios(db: Session):
    for u in USUARIOS_INICIAIS:
        if not db.query(Usuario).filter_by(email=u["email"]).first():
            usuario = Usuario(
                nome=u["nome"],
                email=u["email"],
                senha_hash=get_password_hash(u["senha"]),
                role=u["role"]
            )
            db.add(usuario)
            print(f"🌱 Usuário {u['role']} inserido")


def run():
    with SessionLocal() as db:
        seed_produtos(db)
        seed_usuarios(db)
        db.commit()


if __name__ == "__main__":
    run()
