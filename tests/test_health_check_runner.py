from unittest.mock import patch, Mock
import requests
from src.app.services.health_check_runner import HealthCheckRunner
from src.app.repositories.service_repository import ServiceRepository
from src.app.schemas.health_check_schema import HealthStatus


class TestHealthChecker:
    """Tests para HealthCheckRunner"""
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_up(self, mock_get, db_session, sample_service_data):
        """Test: Service UP (respuesta exitosa)."""
        # Mock de respuesta HTTP exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Crear servicio
        service = ServiceRepository.create(db_session, sample_service_data)
        
        # Hacer check
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result is not None
        assert result.status.value == "UP"
        assert result.code_response == "200"
        assert result.response_time_ms is not None
        assert result.response_time_ms > 0
        assert result.error_message is None
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_down(self, mock_get, db_session, sample_service_data):
        """Test: Service DOWN (error HTTP)."""
        # Mock de respuesta con error 500
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        
        service = ServiceRepository.create(db_session, sample_service_data)
        
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result.status.value == "DOWN"
        assert result.code_response == "500"
        assert result.response_time_ms is not None
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_timeout(self, mock_get, db_session, sample_service_data):
        """Test: Service TIMEOUT."""
        # Mock de timeout
        mock_get.side_effect = requests.Timeout()
        
        service = ServiceRepository.create(db_session, sample_service_data)
        
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result.status.value == "TIMEOUT"
        assert result.code_response == "Timeout"
        assert result.response_time_ms is None
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_connection_error(self, mock_get, db_session, sample_service_data):
        """Test: Service ERROR (error de conexión)."""
        # Mock de error de conexión
        mock_get.side_effect = requests.ConnectionError("DNS resolution failed")
        
        service = ServiceRepository.create(db_session, sample_service_data)
        
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result.status.value == "ERROR"
        assert result.code_response == "Error"
        assert result.response_time_ms is None
        assert result.error_message is not None
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_redirects(self, mock_get, db_session, sample_service_data):
        """Test: Service con redirects (301/302) se considera UP."""
        # Mock de redirect
        mock_response = Mock()
        mock_response.status_code = 200  # requests.get sigue redirects por defecto
        mock_get.return_value = mock_response
        
        service = ServiceRepository.create(db_session, sample_service_data)
        
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result.status.value == "UP"
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_all_active_services_multiple(self, mock_get, db_session):
        """Test: Check de múltiples servicios activos."""
        # Mock de respuesta
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Crear varios servicios activos
        for i in range(3):
            ServiceRepository.create(db_session, {
                "service_name": f"Service {i}",
                "service_url": f"https://example{i}.com",
                "check_interval": 60,
                "is_active": True
            })
        
        # Crear un servicio inactivo (no debería chequearse)
        ServiceRepository.create(db_session, {
            "service_name": "Inactive",
            "service_url": "https://inactive.com",
            "check_interval": 60,
            "is_active": False
        })
        
        results = HealthCheckRunner.check_all_active_services(db_session)
        
        # Solo debería haber chequeado los 3 activos
        assert len(results) == 3
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_all_no_active_services(self, mock_get, db_session):
        """Test: No hay servicios activos para checkear."""
        # Crear solo servicios inactivos
        ServiceRepository.create(db_session, {
            "service_name": "Inactive",
            "service_url": "https://example.com",
            "check_interval": 60,
            "is_active": False
        })
        
        results = HealthCheckRunner.check_all_active_services(db_session)
        
        assert results == []
        # No debería haber llamado a requests.get
        mock_get.assert_not_called()
    
    @patch('src.app.services.health_check_runner.requests.get')
    def test_check_service_404_is_down(self, mock_get, db_session):
        """Test: 404 se considera DOWN, no UP."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        service = ServiceRepository.create(db_session, {
            "service_name": "Test",
            "service_url": "https://example.com/nonexistent",
            "check_interval": 60
        })
        
        result = HealthCheckRunner.check_service(db_session, service)
        
        assert result.status.value == "DOWN"
        assert result.code_response == "404"