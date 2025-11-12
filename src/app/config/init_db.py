from src.app.config.database import engine, Base
from src.app.models.service import Service
from src.app.models.health_check import HealthCheck


def init_database():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind = engine)
    print("Base de datos inicializada")


if __name__ == "__main__":
    init_database()