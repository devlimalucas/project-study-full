import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from infra.database import Base
from infra.deps import get_db
from main import app
from models import Usuario
from core.security_jwt import get_password_hash

# Banco em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Resetar banco antes de cada teste
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Sobrescrever dependência get_db para usar banco de testes
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# Cliente de testes
@pytest.fixture
def client():
    return TestClient(app)


# ------------------------
# Helpers para auth
# ------------------------

@pytest.fixture
def criar_usuario_admin():
    """Cria e retorna um usuário admin no banco de testes."""
    db = TestingSessionLocal()
    admin = Usuario(
        nome="Admin Test",
        email="admin@test.com",
        senha_hash=get_password_hash("admin123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    db.close()
    return admin


@pytest.fixture
def autenticar():
    """Retorna uma função helper para login e token JWT."""
    def _login(client, email: str, senha: str) -> str:
        response = client.post("/auth/login", json={"email": email, "senha": senha})
        data = response.json()
        if response.status_code != 200 or "access_token" not in data:
            raise RuntimeError(f"Falha ao autenticar: {data}")
        return data["access_token"]
    return _login

