from src.app.repositories.service_repository import ServiceRepository


class TestServiceRepository:
    """Tests para ServiceRepository."""
    
    def test_create_service(self, db_session, sample_service_data):
        
        service = ServiceRepository.create(db_session, sample_service_data)
        
        assert service.service_id is not None
        assert service.service_name == "Test Service"
        assert service.is_active is True
    
    def test_get_all_services(self, db_session):
        """Test: Obtener todos los servicios."""
        # Crear varios servicios
        for i in range(3):
            ServiceRepository.create(db_session, {
                "service_name": f"Service {i}",
                "service_url": f"https://example{i}.com",
                "check_interval": 60
            })
        
        services = ServiceRepository.get_all(db_session)
        assert len(services) == 3
    
    def test_get_service_by_id(self, db_session, sample_service_data):
        """Test: Obtener servicio por ID."""
        service = ServiceRepository.create(db_session, sample_service_data)
        
        found = ServiceRepository.get_by_id(db_session, service.service_id)
        assert found is not None
        assert found.service_id == service.service_id
    
    def test_delete_service(self, db_session, sample_service_data):
        """Test: Eliminar servicio."""
        service = ServiceRepository.create(db_session, sample_service_data)
        deleted = ServiceRepository.delete(db_session, service.service_id)
        assert deleted is True
        
        # Verificar que ya no existe
        found = ServiceRepository.get_by_id(db_session, service.service_id)
        assert found is None
