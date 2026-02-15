from pydantic import BaseModel, EmailStr
from typing import Optional


# ==========================================================
# 🔹 ESQUEMA BASE
# ==========================================================
# Contiene los campos comunes que comparten Create, Update y Response.
# Aquí definimos los datos que forman parte del modelo Alumno.

class AlumnoBase(BaseModel):
    nombre: str                     # Nombre obligatorio del alumno
    email: EmailStr                 # Email validado automáticamente por Pydantic
    telefono: Optional[str] = None  # Teléfono opcional
    profesor_id: Optional[int] = None  # FK opcional al profesor


# ==========================================================
# 🔹 ESQUEMA PARA CREAR (POST)
# ==========================================================
# Hereda de AlumnoBase.
# Se usa cuando el cliente envía datos para crear un nuevo alumno.

class AlumnoCreate(AlumnoBase):
    pass


# ==========================================================
# 🔹 ESQUEMA PARA ACTUALIZAR (PUT)
# ==========================================================
# Todos los campos son opcionales para permitir actualizaciones parciales.

class AlumnoUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    profesor_id: Optional[int] = None
    
# ==========================================================
# 🔹 ESQUEMA SIMPLE DE PROFESOR (para usar dentro de Alumno)
# ==========================================================
class ProfesorSimple(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    especialidad: Optional[str] = None

    class Config:
        from_attributes = True
    

# ==========================================================
# 🔹 ESQUEMA DE RESPUESTA (GET)
# ==========================================================
# Incluye el ID generado por la base de datos.
# Se usa para devolver datos al cliente.

class AlumnoResponse(AlumnoBase):
    id: int
    profesor: Optional[ProfesorSimple] = None  # Información del profesor asociado (si existe)  

    class Config:
        from_attributes = True
        # Permite que Pydantic convierta automáticamente
        # objetos SQLAlchemy en modelos de respuesta.

# ========================================================== 
# 🔹 ESQUEMA REDUCIDO PARA USAR DENTRO DE PROFESOR
# ==========================================================
class AlumnoSimple(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    
    class Config:
        from_attributes = True