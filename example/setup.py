from setuptools import setup, find_packages, Command
from schema_codegen.setuptools import schema_codegen_cmd_class
from pathlib import Path


setup(
    name="example",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "schema_codegen",
        "asyncpg",
        "passlib",
        "pydantic-settings",
        "fastapi",
        "bcrypt",
        "uvicorn",
        "greenlet",
        "pytest",
        "httpx",
    ],
    cmdclass={
        "schema_codegen": schema_codegen_cmd_class(
            migrations_dir = Path(__file__).parent / "migrations",
            models_output_dir = Path(__file__).parent / "example" / "models" / "db"
        ),
    },
)
