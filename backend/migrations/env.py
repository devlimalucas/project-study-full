import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Configuração do Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importa o Base direto do infra/database.py
from infra.database import Base

# Importa os módulos dos models para registrar no metadata
import models.produto
import models.usuario
import models.venda

# O Alembic vai usar o metadata do Base
target_metadata = Base.metadata

# Variáveis de ambiente para conexão
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME")

if not all([db_user, db_pass, db_host, db_port, db_name]):
    raise RuntimeError("❌ Variáveis de ambiente do banco não estão completas!")

url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4&ssl_disabled=true"
config.set_main_option("sqlalchemy.url", url)

def run_migrations_offline() -> None:
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
