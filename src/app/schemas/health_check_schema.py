from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

from src.app.models.health_check import HealthStatus


class HealthCheckCreate(BaseModel):
    service_id: UUID
    status: HealthStatus
    response_time_ms: float | None = None
    code_response: str | None = None
    error_message: str | None = None

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "service_id": "132j123-123n1mk1",
                "status": "UP",
                "response_time_ms": 123.5,
                "code_response":"200",
                "error_message": None
                }
                
        }
            
            
class HealthCheckResponse(BaseModel):
    health_check: UUID
    service_id: UUID
    status: HealthStatus
    response_time_ms: float | None
    code_response: str | None
    error_message: str | None
    checked_at: datetime

    class ConfigDict:
        from_attributes: True

class ServiceHealthSumary(BaseModel):
    service_id: UUID
    service_name: str
    current_status: HealthStatus
    last_checked: datetime
    uptime_percentage: float
    avg_response_ms: float | None
