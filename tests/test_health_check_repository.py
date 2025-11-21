from src.app.repositories.service_repository import ServiceRepository
from src.app.repositories.health_check_repository import HealthCheckRepository
from src.app.models.health_check import HealthStatus


class TestHealthCheckRepository:
    """Tests para HealthCheckRepository."""
    
    def test_create_health_check(self, db_session, sample_service_data):
        """Test: Crear un health check."""
        # Primero crear un servicio
        service = ServiceRepository.create(db_session, sample_service_data)
        
        health_check_data = {
        "service_id": service.service_id,
        "status": "UP",
        "response_time_ms": 150.5,
        "code_response": "200",
        "error_message": None
    }

        check = HealthCheckRepository.create(db_session, health_check_data)
        
        assert check.health_check_id is not None
        assert check.service_id == service.service_id
        assert check.status == HealthStatus.UP
    
    def test_get_latest_check(self, db_session, sample_service_data):
        """Test: Obtener el último health check."""
        # Crear servicio
        service = ServiceRepository.create(db_session, sample_service_data)
        
        # Crear varios checks
        for i in range(3):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100 + i,
                "code_response": "200",
                "error_message": None
            })
        
        # Obtener el último
        latest = HealthCheckRepository.get_latest_by_service(
            db_session, 
            service.service_id
        )
        
        assert latest is not None
        assert latest.response_time_ms == 102  # El último creado
    
    def test_get_history(self, db_session, sample_service_data):
        """Test: Obtener historial de checks."""
        service = ServiceRepository.create(db_session, sample_service_data)
        
        # Crear checks
        for i in range(5):
            HealthCheckRepository.create(db_session, {
                "service_id": service.service_id,
                "status": HealthStatus.UP,
                "response_time_ms": 100 + i,
                "code_response": "200",
                "error_message": None
            })
        
        # Obtener historial (limit 3)
        history = HealthCheckRepository.get_history_by_service(
            db_session, 
            service.service_id,
            limit=3
        )
        
        assert len(history) == 3