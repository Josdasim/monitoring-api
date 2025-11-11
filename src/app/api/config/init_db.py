from src.app.api.config.database import engine, Base
from src.app.models.service import Service

def init_database():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(bind = engine)
    print("Base de datos inicializada")


if __name__ == "__main__":
    init_database()