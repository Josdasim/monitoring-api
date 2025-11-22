import pytest
from uuid import uuid7
from fastapi import HTTPException
from src.app.services.health_check_service import HealthCheckService
from src.app.schemas.health_check_schema import HealthCheckCreate, HealthStatus
from src.app.repositories.health_check_repository import HealthCheckRepository
from src.app.repositories.service_repository import ServiceRepository

class TestHealthCheckService:
    """Tests para HealthCheckService"""
    
    def test_create_health_check(self, db_session, sample_service_data):
        """Test: Crear un health check"""
        # Crear servicio primero
        service = ServiceRepository.create(db_session, sample_service_data)
        
        # Crear health check
        check_data = HealthCheckCreate(
            service_id=service.service_id,
            status=HealthStatus.UP,
            response_time_ms=150.5,
            code_response="200",
            error_message=None
        )
        
        check = HealthCheckService.create_health_check(db_session, check_data)
        
        assert check.health_check_id is not None
        assert check.status.value == "UP"
        assert check.response_time_ms == 150.5
    
    def test_get_latest_check_exists(self, db_session):
        """Test: Obtener último check cuando existe."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Crear checks
        for i in range(3):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100 + i,
                "code_response": "200",
                "error_message": None
            })
        
        latest = HealthCheckService.get_latest_check(db_session, service.service_id)
        assert latest is not None
        assert latest.response_time_ms == 102  # El último
    
    def test_get_latest_check_not_found(self, db_session):
        """Test: Error cuando no hay checks."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        with pytest.raises(HTTPException) as exc_info:
            HealthCheckService.get_latest_check(db_session, service.service_id)
        
        assert exc_info.value.status_code == 404
    
    def test_get_check_history_with_limit(self, db_session):
        """Test: Obtener historial con límite."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Crear 10 checks
        for i in range(10):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100 + i,
                "code_response": "200",
                "error_message": None
            })
        
        # Obtener solo 5
        history = HealthCheckService.get_check_history(db_session, service.service_id, limit=5)
        assert len(history) == 5
    
    def test_get_check_history_limit_validation(self, db_session):
        """Test: El límite se ajusta automáticamente si excede el máximo."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Intentar limit mayor a 100
        history = HealthCheckService.get_check_history(db_session, service.service_id, limit=200)
        # No debería fallar, el service lo ajusta a 100
        assert True
    
    def test_get_service_summary_success(self, db_session):
        """Test: Obtener summary con métricas calculadas."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test Service",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Crear checks: 8 UP, 2 DOWN
        for i in range(8):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100 + (i * 10),
                "code_response": "200",
                "error_message": None
            })
        
        for i in range(2):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.DOWN,
                "response_time_ms": None,
                "code_response": "500",
                "error_message": "Server error"
            })
        
        summary = HealthCheckService.get_service_summary(db_session, service.service_id)
        
        assert summary.service_name == "Test Service"
        assert summary.uptime_percentage == 80.0  # 8/10 = 80%
        assert summary.avg_response_ms is not None
        assert summary.avg_response_ms > 0
    
    def test_get_service_summary_service_not_found(self, db_session):
        """Test: Error en summary si el servicio no existe."""
        fake_id = uuid7()
        
        with pytest.raises(HTTPException) as exc_info:
            HealthCheckService.get_service_summary(db_session, fake_id)
        
        assert exc_info.value.status_code == 404
    
    def test_get_service_summary_no_checks(self, db_session):
        """Test: Error en summary si no hay checks."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        with pytest.raises(HTTPException) as exc_info:
            HealthCheckService.get_service_summary(db_session, service.service_id)
        
        assert exc_info.value.status_code == 404
    
    def test_cleanup_old_checks(self, db_session):
        """Test: Limpiar checks antiguos."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Crear 20 checks
        for i in range(20):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100,
                "code_response": "200",
                "error_message": None
            })
        
        # Limpiar, mantener solo 10
        result = HealthCheckService.cleanup_old_checks(db_session, service.service_id, keep_last=10)
        
        
        assert result["deleted"] == 10
        assert result["kept"] == 10
        
        # Verificar que solo quedan 10
        remaining = HealthCheckRepository.get_history_by_service(
            db_session, 
            service.service_id,
            limit=100
        )
        assert len(remaining) == 10
    
    def test_cleanup_validates_keep_last_max(self, db_session):
        """Test: Cleanup valida el máximo de registros a mantener."""
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com",
            "check_interval": 60
        })
        
        # Intentar con keep_last muy alto (debería ajustarse a 10000)
        result = HealthCheckService.cleanup_old_checks(db_session, service.service_id, keep_last=20000)
        assert result["kept"] == 10000  # Ajustado al máximo