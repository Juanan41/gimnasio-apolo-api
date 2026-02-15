from pydantic import BaseModel, EmailStr, Field
from app.schemas.alumno import AlumnoSimple
from typing import List
from typing import Optional

# Esquema para representar un profesor

class ProfesorBase(BaseModel):
    nombre: str
    email: EmailStr
    especialidad: Optional[str] = None

# Esquema para crear un nuevo profesor(POST), hereda de ProfesorBase y no añade campos adicionales por ahora.

class ProfesorCreate(ProfesorBase):
    pass

# Esquema para actualizar un profesor existente (PUT), hereda de ProfesorBase pero hace todos los campos opcionales para permitir actualizaciones parciales.
class ProfesorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    especialidad: Optional[str] = None
    
# Esquema para devolver un profesor (GET), incluye el ID y una lista de alumnos asociados.
class ProfesorResponse(ProfesorBase):
    id: int
    alumnos: List[AlumnoSimple] = Field(default_factory=list)  # Lista de alumnos asociados al profesor    
   
    class Config:
        from_attributes = True  # Permite crear el modelo a partir de un objeto SQLAlchemy.