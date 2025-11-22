from datetime import datetime
from uuid import UUID
from src.app.models.service import Service
from src.app.models.health_check import HealthCheck, HealthStatus


class TestHealthCheckModel:
    """Tests para el modelo HealthCheck."""
    
    def test_create_health_check_model(self, db_session):
        """Test: Crear una instancia de HealthCheck."""
        # Primero crear un servicio
        service = Service(
            service_name="Test",
            service_url="https://example.com"
        )
        db_session.add(service)
        db_session.commit()
        
        # Crear health check
        check = HealthCheck(
            service_id=service.service_id,
            status=HealthStatus.UP,
            response_time_ms=150.5,
            code_response="200"
        )
        
        db_session.add(check)
        db_session.commit()
        db_session.refresh(check)
        
        assert check.health_check_id is not None
        assert isinstance(check.health_check_id, UUID)
        assert check.status == HealthStatus.UP
        assert check.response_time_ms == 150.5
        assert isinstance(check.checked_at, datetime)
    
    def test_health_check_with_error(self, db_session):
        """Test: HealthCheck con error."""
        service = Service(
            service_name="Test",
            service_url="https://example.com"
        )
        db_session.add(service)
        db_session.commit()
        
        check = HealthCheck(
            service_id=service.service_id,
            status=HealthStatus.ERROR,
            response_time_ms=None,
            code_response="Error",
            error_message="Connection refused"
        )
        
        db_session.add(check)
        db_session.commit()
        db_session.refresh(check)
        
        assert check.status == HealthStatus.ERROR
        assert check.response_time_ms is None
        assert check.error_message == "Connection refused"
    
    def test_health_check_relationship(self, db_session):
        """Test: Relación entre Service y HealthCheck."""
        service = Service(
            service_name="Test",
            service_url="https://example.com"
        )
        db_session.add(service)
        db_session.commit()
        
        # Crear varios checks para el mismo servicio
        for i in range(3):
            check = HealthCheck(
                service_id=service.service_id,
                status=HealthStatus.UP,
                response_time_ms=100 + i,
                code_response="200"
            )
            db_session.add(check)
        
        db_session.commit()
        db_session.refresh(service)
        
        # Verificar relación
        assert len(service.health_checks) == 3
    
    def test_health_status_enum_values(self):
        """Test: Valores del enum HealthStatus."""
        assert HealthStatus.UP.value == "UP"
        assert HealthStatus.DOWN.value == "DOWN"
        assert HealthStatus.TIMEOUT.value == "TIMEOUT"
        assert HealthStatus.ERROR.value == "ERROR"