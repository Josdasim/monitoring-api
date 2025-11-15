import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar conexion con el motor de la DB
engine = create_engine(
    DATABASE_URL,
    echo = False,
    pool_pre_ping = True

)

# Configuracion de creacion de sesiones
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