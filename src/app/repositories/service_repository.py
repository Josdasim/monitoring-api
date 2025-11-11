from sqlalchemy.orm import Session
from src.app.models.service import Service
from uuid import UUID

class ServiceRepository:

    @staticmethod
    def create(db:Session, service_data: dict) -> Service:
        """Crea un nuevo servicio"""
        service = Service(**service_data)
        db.add(service)
        db.commit()
        db.refresh(service) # Actualizar con los datos de la DB
        return service
    
    @staticmethod
    def get_all(db:Session, skip:int = 0, limit:int = 100) -> list[Service]:
        """Lista todos los servicios registrados"""
        return db.query(Service).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db:Session, service_id:UUID) -> Service:
        """Obtiene un servicio por ID"""
        return db.query(Service).filter(Service.service_id == service_id).first()
    
    #TODO: Metodo para actualizar datos en caso de que se quiera hacer

    @staticmethod
    def delete(db:Session, service_id:UUID) -> bool:
        """Elimina un servicio por ID"""
        service = db.query(Service).filter(Service.service_id == service_id).first()
        if service:
            db.delete(service)
            db.commit()
            return True
        return False
