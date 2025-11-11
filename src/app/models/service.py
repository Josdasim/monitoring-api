from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

class Service():
    __tablename__ = "services"

    service_id = Column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid7)
    service_name = Column(String, nullable = False)
    service_url = Column(String, nullable = False)
    is_active = Column(Boolean, default = True)
    check_interval = Column(Integer, default = 300)
    created_at = Column(DateTime, default = datetime.now)
    updated_at = Column(DateTime, defailt = datetime.now, onupdate=datetime.now)
    

