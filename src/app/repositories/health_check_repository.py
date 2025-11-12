from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from src.app.models.health_check import HealthCheck, HealthStatus
from uuid import UUID


class HealthCheckRepository:

    @staticmethod
    def create(db:Session, health_check_data: dict) -> HealthCheck:
        """Crea un nuevo registro de health check (uso interno)"""
        health_check = HealthCheck(**health_check_data)
        db.add(health_check)
        db.commit()
        db.refresh(health_check)
        return health_check
    
    @staticmethod
    def get_latest_by_service(db:Session, service_id: UUID) -> HealthCheck:
        """Obtiene el ultimo health check de un servicio"""
        return db.query(HealthCheck).filter(HealthCheck.service_id == service_id)\
            .order_by(desc(HealthCheck.checked_at)).first()
    
    @staticmethod
    def get_history_by_service(db:Session, service_id: UUID, limit:int=50) -> list[HealthCheck]:
        """Obtiene el historial de health checks"""
        return db.query(HealthCheck).filter(HealthCheck.service_id == service_id)\
            .limit(limit).all()
    
    @staticmethod
    def get_recent_by_service(db:Session, service_id:UUID, limit:int=100) -> list[HealthCheck]:
        """Obtiene los checks recientes para calcular metricas"""
        return db.query(HealthCheck).filter(HealthCheck.service_id == service_id)\
            .order_by(desc(HealthCheck.checked_at)).limit(limit).all()
    
    @staticmethod
    def get_avg_response_time(db: Session, service_id:UUID, limit:int=100) -> float:
        subquery = db.query(HealthCheck.response_time_ms)\
            .filter(HealthCheck.service_id == service_id,
                    HealthCheck.response_time_ms.isnot(None))\
            .order_by(desc(HealthCheck.checked_at)).limit(limit).subquery()
        
        result = db.query(func.avg(subquery.c.response_time_ms)).scalar()
        return float(result if result else None)
    
    @staticmethod
    def delete_old_checks(db: Session, service_id: UUID, keep_last:int = 1000):
        """Elimina checks antiguos, par matener los ultimos n"""
        subquery = db.query(HealthCheck.service_id).filter(HealthCheck.service_id==service_id)\
            .order_by(desc(HealthCheck.checked_at)).limit(keep_last).subquery()
        
        deleted = db.query(HealthCheck)\
            .filter(HealthCheck.service_id == service_id,
                    HealthCheck.health_check_id.not_in_(subquery))\
            .delete(synchronize_session=False)
        
        db.commit()
        return deleted