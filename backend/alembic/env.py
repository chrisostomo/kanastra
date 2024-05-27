import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool
from alembic import context

# Adiciona o caminho do aplicativo ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importa a configuração do banco de dados e os modelos
from app.models.db import Base, DATABASE_URL
from app.models.debt import Debt
from app.models.csv_file import CsvFile

# Carrega a configuração do arquivo .ini
config = context.config

# Interpreta a configuração do arquivo .ini de logging do aplicativo
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adiciona a URL do banco de dados à configuração do Alembic
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Alvo das migrações
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
