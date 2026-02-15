from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from typing import List

from app.database import get_db
from app.models.alumno import Alumno
from app.models.profesor import Profesor  # Importamos el modelo Profesor para validar profesor_id
from app.schemas.alumno import (
    AlumnoCreate,
    AlumnoUpdate,
    AlumnoResponse
)

# Creamos un router para el alumno
router = APIRouter(
    prefix="/alumnos",
    tags=["alumnos"]
)


# GET: Obtener todos los alumnos
@router.get("/", response_model=List[AlumnoResponse])
def get_alumnos(db: Session = Depends(get_db)):
    
    """
    Devuelve todos los alumnos registrados en la base de datos.
    """
    
    return db.query(Alumno).all()

# GET: Obtener alumno por ID
@router.get("/{alumno_id}", response_model=AlumnoResponse)
def get_alumno(alumno_id: int, db: Session = Depends(get_db)):
    
    """
    Devuelve un alumno específico por su ID.
    """
    
    alumno = db.query(Alumno).options(joinedload(Alumno.profesor)).filter(Alumno.id == alumno_id).first()
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    return alumno

# POST: Crear un nuevo alumno
@router.post("/", response_model=AlumnoResponse)
def create_alumno(alumno_data: AlumnoCreate, db: Session = Depends(get_db)):
    
    """
    Crea un nuevo alumno validando que el profesor exista (si se envía profesor_id).
    """
    # Si enviamos profesor_id, verificamos que el profesor exista
    if alumno_data.profesor_id:
        profesor = db.query(Profesor).filter(Profesor.id == alumno_data.profesor_id).first()
        if not profesor:
            raise HTTPException(status_code=400, detail="El profesor asignado no existe")
    
    nuevo_alumno = Alumno(**alumno_data.model_dump())
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)
    return nuevo_alumno

# PUT: Actualizar un alumno existente
@router.put("/{alumno_id}", response_model=AlumnoResponse)
def update_alumno(alumno_id: int, alumno_data: AlumnoUpdate, db: Session = Depends(get_db)):
    
    """
    Actualiza un alumno existente con los datos proporcionados.
    Permite actualizaciones parciales.
    """
    
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
     # Solo actualiza los campos enviados (exclude_unset=True)
    for key, value in alumno_data.model_dump(exclude_unset=True).items():
        setattr(alumno, key, value)
    
    db.commit()
    db.refresh(alumno)
    return alumno

# DELETE: Eliminar un alumno
@router.delete("/{alumno_id}")
def delete_alumno(alumno_id: int, db: Session = Depends(get_db)):
    
    """
    Elimina un alumno específico por su ID.
    """
    
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    
    db.delete(alumno)
    db.commit()

    return {"message": "Alumno eliminado exitosamente"}