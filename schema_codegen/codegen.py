import subprocess

from pathlib import Path
from testcontainers.postgres import PostgresContainer

from schema_codegen.migrations import apply_migrations


class SchemaCodeGen:
    def __init__(self, migrations_dir: Path, models_output_dir: Path):
        """
        Initialize the SchemaCodeGen tool.

        :param migrations_dir: Path to the Flyway migrations directory.
        :param models_output_dir: Path where the generated SQLAlchemy models will be saved.
        """
        self.migrations_dir = migrations_dir.resolve()
        self.models_output_dir = models_output_dir.resolve()
        self.models_output_dir.mkdir(parents=True, exist_ok=True)

    def start_postgres(self) -> PostgresContainer:
        """Start a Postgres container and return the instance."""
        postgres = PostgresContainer("postgres:15")
        postgres.start()
        return postgres

    def generate_models(self, postgres_url: str):
        """Generate SQLAlchemy models."""
        output_file = self.models_output_dir / "__init__.py"
        subprocess.run(
            ["sqlacodegen", postgres_url, "--outfile", str(output_file)],
            check=True,
        )

    def run(self):
        """Run the complete code generation process."""
        postgres = self.start_postgres()
        postgres_url = postgres.get_connection_url()

        try:
            apply_migrations(self.migrations_dir, postgres_url)
            self.generate_models(postgres_url)
        finally:
            postgres.stop()
