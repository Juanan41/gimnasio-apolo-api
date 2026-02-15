# Importamos tipos de columnas y ForeignKey para crear relaciones
from sqlalchemy import Column, Integer, String, ForeignKey

# Importamos relationship para enlazar con el modelo Profesor
from sqlalchemy.orm import relationship

# Importamos la Base declarativa
from app.database import Base


# Definimos la clase Alumno que representa la tabla "alumnos"
class Alumno(Base):

    # Nombre real de la tabla en PostgreSQL
    __tablename__ = "alumnos"

    # Clave primaria autoincremental
    id = Column(Integer, primary_key=True, index=True)

    # Nombre del alumno (obligatorio)
    nombre = Column(String(100), nullable=False)

    # Email único del alumno
    email = Column(String(150), unique=True, nullable=False)

    # Teléfono opcional
    telefono = Column(String(20), nullable=True)

    # Clave foránea:
    # Relaciona alumno con un profesor
    # Hace referencia a la tabla "profesores" columna "id"
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=True)

    # Relación Many-to-One:
    # Cada alumno tiene un profesor
    profesor = relationship("Profesor", back_populates="alumnos")
