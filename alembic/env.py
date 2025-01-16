from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your metadata here
from app.database import Base  # Update with the correct path to your models
target_metadata = Base.metadata

# Interpret the config file for Python logging.
fileConfig(context.config.config_file_name)

# Set up the database URL
config = context.config
config.set_main_option("sqlalchemy.url", "postgresql://postgres:nimble123@localhost:5432/blogfinal")  # Update with your URL

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
