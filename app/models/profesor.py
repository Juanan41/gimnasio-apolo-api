# Importamos los tipos de columnas que vamos a utilizar
from sqlalchemy import Column, Integer, String

# Importamos relationship para definir relaciones entre tablas
from sqlalchemy.orm import relationship

# Importamos la Base declarativa creada en database.py
from app.database import Base


# Definimos la clase Profesor que representa la tabla "profesores"
class Profesor(Base):

    # Nombre real de la tabla en PostgreSQL
    __tablename__ = "profesores"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del profesor (obligatorio)
    nombre = Column(String(100), nullable=False)

    # Email único (no puede repetirse)
    email = Column(String(150), unique=True, nullable=False)

    # Especialidad del profesor (opcional)
    especialidad = Column(String(100), nullable=True)

    # Relación One-to-Many:
    # Un profesor puede tener varios alumnos
    alumnos = relationship("Alumno", back_populates="profesor")
