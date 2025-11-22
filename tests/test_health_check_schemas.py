from uuid import uuid7
from datetime import datetime
from src.app.schemas.health_check_schema import (
    HealthCheckCreate,
    HealthStatus,
    ServiceHealthSummary
)


class TestHealthCheckSchemas:
    """Tests para schemas de HealthCheck."""
    
    def test_health_check_create_valid(self):
        """Test: HealthCheckCreate con datos válidos."""
        data = {
            "service_id": uuid7(),
            "status": HealthStatus.UP,
            "response_time_ms": 150.5,
            "code_response": "200",
            "error_message": None
        }
        
        schema = HealthCheckCreate(**data)
        
        assert schema.status == HealthStatus.UP
        assert schema.response_time_ms == 150.5
    
    def test_health_check_create_with_error(self):
        """Test: HealthCheckCreate con error."""
        data = {
            "service_id": uuid7(),
            "status": HealthStatus.ERROR,
            "response_time_ms": None,
            "code_response": "Error",
            "error_message": "Connection refused"
        }
        
        schema = HealthCheckCreate(**data)
        
        assert schema.status == HealthStatus.ERROR
        assert schema.response_time_ms is None
        assert schema.error_message == "Connection refused"
    
    def test_health_status_enum(self):
        """Test: HealthStatus tiene todos los valores."""
        assert HealthStatus.UP == "UP"
        assert HealthStatus.DOWN == "DOWN"
        assert HealthStatus.TIMEOUT == "TIMEOUT"
        assert HealthStatus.ERROR == "ERROR"
    
    def test_service_health_summary_valid(self):
        """Test: ServiceHealthSummary con datos válidos."""
        data = {
            "service_id": uuid7(),
            "service_name": "Test Service",
            "current_status": HealthStatus.UP,
            "last_checked": datetime.now(),
            "uptime_percentage": 98.5,
            "avg_response_ms": 145.23
        }
        
        schema = ServiceHealthSummary(**data)
        
        assert schema.service_name == "Test Service"
        assert schema.uptime_percentage == 98.5
        assert schema.avg_response_ms == 145.23
    
    def test_service_health_summary_no_avg_response(self):
        """Test: ServiceHealthSummary sin avg_response_ms."""
        data = {
            "service_id": uuid7(),
            "service_name": "Test",
            "current_status": HealthStatus.DOWN,
            "last_checked": datetime.now(),
            "uptime_percentage": 50.0,
            "avg_response_ms": None
        }
        
        schema = ServiceHealthSummary(**data)
        
        assert schema.avg_response_ms is None