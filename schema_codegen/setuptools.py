from pathlib import Path
from setuptools import Command

from schema_codegen.codegen import SchemaCodeGen

def schema_codegen_cmd_class(migrations_dir: Path, models_output_dir: Path) -> Command:
    class SchemaCodeGenCmd(Command):
        """Custom command to handle migrations and generate SQLAlchemy models."""
        description = "Run migrations and generate SQLAlchemy models."
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            # Use SchemaCodeGen to perform the process
            codegen = SchemaCodeGen(migrations_dir, models_output_dir)
            codegen.run()
    
    return SchemaCodeGenCmd