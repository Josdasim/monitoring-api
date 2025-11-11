from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#De momento se manejara con sqlite
SQLALCHEMY_DATABASE_URL = "sqlite:///./monitoring.db"

# Motor de la DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False} #Solo para test en sqlite
)

# Crear sesiones
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

# Clase para los modelos
Base = declarative_base()

# Dependencia para FastAPI
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()