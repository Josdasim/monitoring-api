from sqlalchemy.orm import Session
from src.app.repositories.service_repository import ServiceRepository
from src.app.schemas.service_schema import ServiceCreate
from src.app.models.service import Service
from uuid import UUID


class ServiceServices:
    
    @staticmethod
    def create_service(db: Session, service: ServiceCreate) -> Service:
        """Crea un nuevo servicio"""
        service_dict = service.model_dump()
        return ServiceRepository.create(db, service_dict)
    
    @staticmethod
    def list_services(db: Session, skip:int = 0, limit: int = 100) ->list[Service]:
        """Lista los servicios"""
        return ServiceRepository.get_all(db, skip, limit)
    
    @staticmethod
    def get_service(db: Session, service_id:UUID) -> Service:
        """Obtiene un servicio por ID"""
        service = ServiceRepository.get_by_id(db,service_id)
        if not service:
            # Considerar crear excepciones y mensajes personalizados
            raise ValueError(f"Servicio {service_id} no encontrado")
        return service
    
    @staticmethod
    def delete_service(db: Session, service_id:UUID)-> dict:
        """Elimina un servicio por ID"""
        deleted = ServiceRepository.delete(db,service_id)
        if not deleted:
            # Considerar crear excepciones y mensajes personalizados
            raise ValueError(f"Servicio {service_id} no pudo ser borrado")
        return {"message": "Servicio eliminado correctamente"}
