from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de conexión a la base de datos PostgreSQL, dentro de un contenedor Docker.
DATABASE_URL = "postgresql+psycopg://postgres:postgres@db:5432/gimnasio_apolo_V"

# Crear el motor de la base de datos.
engine = create_engine(DATABASE_URL)

# Crear una sesión para interactuar con la base de datos.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos de SQLAlchemy.
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos en las rutas de FastAPI.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

