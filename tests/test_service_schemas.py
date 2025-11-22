from uuid import uuid7
from pydantic import ValidationError
from datetime import datetime
from src.app.schemas.service_schema import ServiceCreate, ServiceResponse


class TestServiceSchemas:
    """Tests para schemas de Service."""
    
    def test_service_create_valid(self, sample_service_data):
        """Test: ServiceCreate con datos válidos."""
        
        schema = ServiceCreate(**sample_service_data)
        
        assert schema.service_name == "Test Service"
        assert schema.service_url == "https://example.com"
        assert schema.check_interval == 60
    
    def test_service_create_with_defaults(self):
        """Test: ServiceCreate usa valores por defecto."""
        data = {
            "service_name": "Test",
            "service_url": "https://example.com"
        }
        
        schema = ServiceCreate(**data)
        
        assert schema.check_interval == 300  # Default
    
    def test_service_create_invalid_url(self):
        """Test: ServiceCreate rechaza URLs inválidas."""
        data = {
            "service_name": "Test",
            "service_url": "not-a-url",
            "check_interval": 60
        }
        
        schema = ServiceCreate(**data)
        assert schema.service_url == "not-a-url"
    
    def test_service_response_from_dict(self):
        """Test: ServiceResponse se crea desde dict."""
        data = {
            "service_id": uuid7(),
            "service_name": "Test",
            "service_url": "https://example.com",
            "is_active": True,
            "check_interval": 60,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        schema = ServiceResponse(**data)
        
        assert schema.service_name == "Test"
        assert schema.is_active is True

