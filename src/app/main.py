from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.api.v1.endpoints import services, health_checks
from src.app.services.scheduler_service import health_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicacion"""
    print("Iniciando Monitoring API...")
    health_scheduler.start_monitoring(interval_seconds=60)
    print("API ready")

    yield

    print("Apagando...")
    health_scheduler.stop_monitoring()
    print("¡Apagado!")


app = FastAPI(
    title = "Monitoring API",
    description = "API para monitorear servicios",
    version="1.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(services.router, prefix="/api/v1")
app.include_router(health_checks.router, prefix="/api/v1")

@app.get("/")
def root():
    """Endpoint Raiz"""
    return {
        "message":"Monitoring API is running",
        "version":"1.0.0",
        "docs":"/docs"
        }

@app.get("/health")
def health_check():
    """Health check de la propia API"""
    return {"status":"healthy"}
