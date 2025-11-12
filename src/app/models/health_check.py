from sqlalchemy import Column, Float, String, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

import uuid
import enum
from datetime import datetime
from src.app.config.database import Base

class HealthStatus(str, enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"

class HealthCheck(Base):
    __tablename__ = "health_checks"

    health_check_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.service_id"), nullable=False)
    status = Column(SQLEnum(HealthStatus), nullable=False)
    response_time_ms = Column(Float, nullable=True) # En milisegundos
    code_response = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.now, nullable=False)


    service = relationship("Service", back_populates="health_checks")

    def __repr__(self):
        return f"<HealthCheck {self.status} at {self.checked_at}>"