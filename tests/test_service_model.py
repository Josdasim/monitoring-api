from datetime import datetime
from uuid import UUID
from src.app.models.service import Service


class TestServiceModel:
    """Tests para el modelo Service."""
    
    def test_create_service_model(self, db_session, sample_service_data):
        """Test: Crear una instancia de Service."""
        service = Service(**sample_service_data)
        
        db_session.add(service)
        db_session.commit()
        db_session.refresh(service)
        
        assert service.service_id is not None
        assert isinstance(service.service_id, UUID)
        assert service.service_name == "Test Service"
        assert service.is_active is True
        assert isinstance(service.created_at, datetime)
    
    def test_service_defaults(self, db_session):
        """Test: Valores por defecto del modelo Service."""
        service = Service(
            service_name="Test",
            service_url="https://example.com"
        )
        
        db_session.add(service)
        db_session.commit()
        db_session.refresh(service)
        
        assert service.is_active is True  # Default
        assert service.check_interval == 300  # Default 5 min
    
    def test_service_repr(self, db_session):
        """Test: Representación string del modelo."""
        service = Service(
            service_name="Test Service",
            service_url="https://example.com"
        )
        
        db_session.add(service)
        db_session.commit()
        
        assert "Test Service" in repr(service)


