from sqlalchemy.orm import Session
from src.app.repositories.health_check_repository import HealthCheckRepository
from src.app.repositories.service_repository import ServiceRepository
from src.app.models.health_check import HealthStatus
from src.app.schemas.health_check_schema import HealthCheckCreate, ServiceHealthSummary
from uuid import UUID
from fastapi import HTTPException


class HealthCheckService:
    
    @staticmethod
    def create_health_check(db:Session, health_check: HealthCheckCreate):
        health_check_dict = health_check.model_dump()
        return HealthCheckRepository.create(db, health_check_dict)

    @staticmethod
    def get_latest_check(db: Session, service_id: UUID):
        """Obtiene el ultimo health check con validacion"""
        latest_check = HealthCheckRepository.get_latest_by_service(db, service_id)
        if not latest_check:
            raise HTTPException(
                status_code=404,
                # Crear mensaje personalizado
                detail=f"No se encontraron health checks para el servicio {service_id}"
            )
        return latest_check
    
    @staticmethod
    def get_check_history(db: Session, service_id:UUID, limit:int = 50):
        """Obtiene el historial de checks con un limite variado"""
        if limit > 100:
            limit = 100
        return HealthCheckRepository.get_history_by_service(db, service_id, limit)
    
    @staticmethod
    def get_service_summary(db:Session, service_id:UUID) -> ServiceHealthSummary:
        """Genera un resumen con metricas calculadas"""
        service = ServiceRepository.get_by_id(db, service_id)
        if not service:
            raise HTTPException(
                status_code=404,
                detail=f"El servicio '{service_id}' no fue encontrado"
            )
        
        latest = HealthCheckRepository.get_latest_by_service(db, service_id)
        if not latest:
            raise HTTPException(
                status_code=404,
                # Crear mensaje personalizado
                detail=f"No se encontraron health checks para el servicio {service_id}"
            )
        
        recent_checks = HealthCheckRepository.get_recent_by_service(db, service_id, limit=100)

        # Se calcula el porcentaje de tiempo en que el servicio esta arriba
        total = len(recent_checks)
        up_count = sum(1 for check in recent_checks if check.status == HealthStatus.UP)
        uptime = (up_count / total * 100) if total > 0 else 0


        # Promedio de tiempo de respuesta
        avg_response = HealthCheckRepository.get_avg_response_time(
            db, service_id, limit=100
        )

        return ServiceHealthSummary(
            service_id = service.service_id,
            service_name = service.service_name,
            current_status = latest.status,
            last_checked = latest.checked_at,
            uptime_percentage = round(uptime, 2),
            avg_response_ms = round(avg_response, 2) if avg_response else None
        )
    
    @staticmethod
    def cleanup_old_checks(db:Session, service_id: UUID, keep_last:int = 1000):
        """Limpia checks antiguos con validaciones"""
        if keep_last < 100:
            keep_last = 100
        if keep_last > 10000:
            keep_last = 10000

        deleted = HealthCheckRepository.delete_old_checks(db, service_id,keep_last)
        return {
            "deleted":deleted,
            "kept": keep_last,
            "message":f"Eliminados health check antiguos, se mantuvieron los ultimos {keep_last}"
        }