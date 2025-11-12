from fastapi import FastAPI
from src.app.api.v1.endpoints import services


app = FastAPI(
    title = "Monitoring API",
    description = "API para monitorear servicios",
    version="0.1.0"
)

# Incluir routers
app.include_router(services.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message":"Monitoring API is running"}

@app.get("/health")
def health_check():
    return {"status":"healthy"}
