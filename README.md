# Monitoring API 

API para monitoreo de servicios (APIs, sitios web, microservicios)

Este proyecto sera desarrollado con **FastAPI** y permitira:
- Registrar servicios (URLs) para su monitoreo.
- Ejecutar verificaciones automaticas.
- Almacenar resultados como latencia, codigo de respuesta y estado del servicio.

A futuro se podria incluir:
- Logs centralizados.
- Alertas automaticas.

## Arquitectura inical

models/          # Modelos de dominio
repositories/    # Capa de acceso de datos
services/        # Logica de negocio
routers/         # Endpoints

## Tecnologias

- **Python 3.12.3**
- **FastAPI**
