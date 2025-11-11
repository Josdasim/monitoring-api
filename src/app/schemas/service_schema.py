from pydantic import BaseModel, HttpUrl
from datetime import datetime
from uuid import UUID


# Para crear un servicio (input del usuario)
class ServiceCreate(BaseModel):
    service_name: str
    service_url: str
    check_interval: int = 300

    class configDict:
        json_schema_extra = {
            "example":{
                "service_name": "My API",
                "service_url": "https://api.example.com/health",
                "check_interval": 300
            }
        }


# Para responder (output al usuario)
class ServiceResponse(BaseModel):
    service_id: UUID
    service_name: str
    service_url: str
    is_active: bool
    check_interval: int
    created_at: datetime
    updated_at: datetime

    class configDict:
        from_attributes = True