import subprocess

from os import environ
from urllib.parse import urlparse


def apply_migrations(migrations_dir: str, postgres_url: str):
    url = urlparse(postgres_url)
    env_vars = {
        "PYWAY_DATABASE_HOST": url.hostname,
        "PYWAY_DATABASE_PORT": '%s' % url.port,
        "PYWAY_DATABASE_NAME": url.path.lstrip('/'),
        "PYWAY_DATABASE_USERNAME": url.username,
        "PYWAY_DATABASE_PASSWORD": url.password,
        "PYWAY_TYPE": "postgres",
        "PYWAY_TABLE": "schema_history",
        "PYWAY_DATABASE_MIGRATION_DIR": migrations_dir
    }

    env = environ.copy()
    env.update(env_vars)
    
    subprocess.run(["pyway", "migrate"], check=True, env=env)