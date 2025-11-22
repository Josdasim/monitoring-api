import requests
from datetime import datetime
from sqlalchemy.orm import Session
from src.app.models.health_check import HealthStatus
from src.app.models.service import Service
from src.app.services.health_check_service import HealthCheckService
from src.app.schemas.health_check_schema import HealthCheckCreate
import time

class HealthCheckRunner:
    """Core logico: realiza health checks HTTP a servicios monitoreados"""

    @staticmethod
    def check_service(db: Session, service: Service):
        """Realiza un health check a un servicio especifico"""
        print(f"Revisando {service.service_name} ({service.service_url})...")

        start_time = time.time()

        try:
            # Intento de conexion HTTP
            response = requests.get(
                service.service_url,
                timeout=10,
                allow_redirects=True
            )

            response_time_ms = (time.time() - start_time) * 1000

            # Determinar el estado basado en el status code
            if 200 <= response.status_code < 300:
                status = HealthStatus.UP
            else:
                status = HealthStatus.DOWN

            health_check = HealthCheckCreate(
                service_id = service.service_id,
                status = status,
                response_time_ms = round(response_time_ms, 2),
                code_response = str(response.status_code),
                error_message = None
            )

            print(f"{service.service_name}: {status.value} "
                  f"({response.status_code}) - {response_time_ms:.0f}ms")
            
        except requests.Timeout:
            # Caso: timeout (no respondió a tiempo)
            health_check = HealthCheckCreate(
                service_id = service.service_id,
                status = HealthStatus.TIMEOUT,
                response_time_ms = None,
                code_response = "Timeout",
                error_message = "Tiempo de espera superado..."
            )
            print(f"{service.service_name}: TIMEOUT")
            
        except requests.RequestException as e:
            # Caso: error de conexión
            health_check = HealthCheckCreate(
                service_id=service.service_id,
                status=HealthStatus.ERROR,
                response_time_ms=None,
                code_response="Error",
                error_message=str(e)[:500]
            )
            print(f"{service.service_name}: ERROR - {str(e)[:100]}")
        
        # Guardar en DB con validación
        return HealthCheckService.create_health_check(db, health_check)
    
    @staticmethod
    def check_all_active_services(db: Session):
        """Verifica todos los servicios activos."""
        services = db.query(Service).filter(Service.is_active == True).all()
        
        if not services:
            print("No hay servicios activos que revisar")
            return []
        
        print(f"Iniciando revision de estado de {len(services)} servicios...")
        results = []
        
        for service in services:
            result = HealthCheckRunner.check_service(db, service)
            results.append(result)
        
        print(f"Se completaron {len(results)} revisiones\n")
        return results