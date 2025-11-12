from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.app.config.database import get_db
from src.app.services.service_services import ServiceServices
from src.app.schemas.service_schema import ServiceCreate, ServiceResponse

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Crea un nuevo servicio para monitorear"""
    try:
        return ServiceServices.create_service(db, service)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{service_id}", response_model=ServiceResponse, status_code=status.HTTP_200_OK)
def get_service(service_id:UUID, db:Session = Depends(get_db)):
    """Obtiene un servicio especifico"""
    try:
        return ServiceServices.get_service(db, service_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/", response_model=list[ServiceResponse], status_code=status.HTTP_200_OK)
def list_services(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    """Lista todos los servicios"""
    return ServiceServices.list_services(db,skip,limit)

@router.delete("/{service_id}", status_code=status.HTTP_200_OK)
def delete_service(service_id:UUID, db:Session = Depends(get_db)):
    """Elimina un servicio"""
    try:
        return ServiceServices.delete_service(db, service_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))