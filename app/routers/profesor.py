from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.profesor import Profesor
from app.schemas.profesor import (
    ProfesorCreate,
    ProfesorUpdate,
    ProfesorResponse
)

# Creamos un router para el profesor
router = APIRouter(
    prefix="/profesores",
    tags=["profesores"]
)

# GET: Obtener profesor por ID
@router.get("/{profesor_id}", response_model=ProfesorResponse)
def get_profesor(profesor_id: int, db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

# POST: Crear un nuevo profesor
@router.post("/", response_model=ProfesorResponse)
def create_profesor(profesor_data: ProfesorCreate, db: Session = Depends(get_db)):
    nuevo_profesor = Profesor(**profesor_data.model_dump())
    db.add(nuevo_profesor)
    db.commit()
    db.refresh(nuevo_profesor)
    return nuevo_profesor

# PUT: Actualizar un profesor existente
@router.put("/{profesor_id}", response_model=ProfesorResponse)
def update_profesor(profesor_id: int, profesor_data: ProfesorUpdate, db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    for key, value in profesor_data.model_dump(exclude_unset=True).items():
        setattr(profesor, key, value)
    
    db.commit()
    db.refresh(profesor)
    return profesor

# DELETE: Eliminar un profesor
@router.delete("/{profesor_id}")
def delete_profesor(profesor_id: int, db: Session = Depends(get_db)):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()
    
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    db.delete(profesor)
    db.commit()
    return {"detail": "Profesor eliminado exitosamente"}