import pytest
from uuid import uuid7
from src.app.services.service_services import ServiceServices
from src.app.schemas.service_schema import ServiceCreate


class TestServiceServicess:
    """Tests para ServiceServices"""
    
    def test_create_service_success(self, db_session, sample_service_data):
        """Test: Crear un servicio exitosamente"""
        
        service = ServiceServices.create_service(db_session, ServiceCreate(**sample_service_data))
        
        assert service.service_id is not None
        assert service.service_name == "Test Service"
        assert service.is_active is True
    
    def test_list_services(self, db_session):
        """Test: Listar servicios con paginación."""
        # Crear varios servicios
        for i in range(5):
            ServiceServices.create_service(db_session, ServiceCreate(
                service_name=f"Service {i}",
                service_url=f"https://example{i}.com",
                check_interval=60
            ))
        
        # Listar todos
        services = ServiceServices.list_services(db_session)
        assert len(services) == 5
        
        # Listar con limit
        services_limited = ServiceServices.list_services(db_session, skip=0, limit=3)
        assert len(services_limited) == 3
    
    def test_get_service_exists(self, db_session, sample_service_data):
        """Test: Obtener un servicio que existe."""
        created = ServiceServices.create_service(db_session, ServiceCreate(**sample_service_data))
        
        found = ServiceServices.get_service(db_session, created.service_id)
        assert found.service_id == created.service_id
    
    def test_get_service_not_found(self, db_session):
        """Test: Error al obtener servicio inexistente."""
        fake_id = uuid7()
        
        with pytest.raises(ValueError):
            ServiceServices.get_service(db_session, fake_id)
    
    def test_delete_service_success(self, db_session, sample_service_data):
        """Test: Eliminar servicio exitosamente."""
        created = ServiceServices.create_service(db_session, ServiceCreate(**sample_service_data))
        
        result = ServiceServices.delete_service(db_session, created.service_id)
        assert "message" in result
        
        # Verificar que ya no existe
        with pytest.raises(ValueError):
            ServiceServices.get_service(db_session, created.service_id)
    
    def test_delete_service_not_found(self, db_session):
        """Test: Error al eliminar servicio inexistente."""
        fake_id = uuid7()
        
        with pytest.raises(ValueError):
            ServiceServices.delete_service(db_session, fake_id)

