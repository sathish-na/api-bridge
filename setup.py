from setuptools import setup, find_packages

setup(
    name="api-bridge",
    version="0.1.0",
    description="Auto-generate APIs from your database schema",
    author="Venkat.R",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "psycopg2-binary"
    ],
    entry_points={
        "console_scripts": [
            "db2api-cli=db2api.cli:main", 
        ],
    },
)
