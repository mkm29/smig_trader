from logging.config import fileConfig
from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlmodel import SQLModel
from alembic import context

# Import your Settings class and models here
from smig_trader.common import settings
from smig_trader.models import StockObservation

# Load the Settings
# settings = Settings()
print(settings)

# this is the Alembic Config object, which provides access to the values within the .ini file
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set the target metadata for Alembic migrations
target_metadata = SQLModel.metadata


# Database connection URL from environment variables (via Settings class)
def get_url():
    return settings.database_uri


# Database connection configuration
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        get_url(),
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
