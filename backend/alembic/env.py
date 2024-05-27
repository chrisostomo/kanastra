import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Carrega a configuração do Alembic
config = context.config
fileConfig(config.config_file_name)

# Obtém a URL do banco de dados a partir das variáveis de ambiente
database_url = os.getenv("DATABASE_URL")
config.set_main_option('sqlalchemy.url', database_url)

# Importa seus modelos
from app.models.db import Base
from app.models import file, debt

# Define a metadata dos modelos
target_metadata = Base.metadata

def run_migrations_offline():
    """Executa migrações no modo 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Executa migrações no modo 'online'."""
    connectable = create_engine(config.get_main_option("sqlalchemy.url"))

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
