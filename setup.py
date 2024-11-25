from setuptools import setup, find_packages

setup(
    name="schema-codegen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyway",
        "testcontainers",
        "sqlalchemy",
        "sqlacodegen==3.0.0rc5",
    ],
    description="A tool to generate SQLAlchemy models from database schemas using Pyway and SQLAlchemy.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
