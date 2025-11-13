from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.app.config.database import get_db
from src.app.services.health_check_service import HealthCheckService
from src.app.schemas.health_check_schema import HealthCheckResponse, ServiceHealthSummary

router = APIRouter(prefix="/health", tags=["health-checks"])


@router.get("/{service_id}/latest", response_model=HealthCheckResponse)
def get_latest_check(service_id: UUID, db: Session = Depends(get_db)
):
    """Obtiene el último health check de un servicio."""
    return HealthCheckService.get_latest_check(db, service_id)


@router.get("/{service_id}/history", response_model=List[HealthCheckResponse])
def get_check_history(service_id: UUID, limit: int = 50, db: Session = Depends(get_db)
):
    """Obtiene el historial de health checks."""
    return HealthCheckService.get_check_history(db, service_id, limit)


@router.get("/{service_id}/summary", response_model=ServiceHealthSummary)
def get_service_summary(service_id: UUID, db: Session = Depends(get_db)
):
    """Obtiene un resumen con métricas calculadas."""
    return HealthCheckService.get_service_summary(db, service_id)


@router.delete("/{service_id}/cleanup")
def cleanup_old_checks(service_id: UUID, keep_last: int = 1000, db: Session = Depends(get_db)
):
    """Limpia health checks antiguos (mantenimiento de DB)."""
    return HealthCheckService.cleanup_old_checks(db, service_id, keep_last)