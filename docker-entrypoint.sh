#!/bin/bash

set -e 
echo "Iniciando Monitoring API..."


if [[ $DATABASE_URL == postgresql* ]] then
    echo "Esperando por Postgres..."
    until pg_isready -h $(echo $DATABASE_URL | sed 's/.*@\(.*\):.*/\1/') 2>/dev/null; do
        echo "Postgres no esta disponible"
        sleep 1
    done
    echo "Postgres esta listo"
fi

echo "Ejecutando migraciones de bases de datos..."
alembic upgrade head

echo "Migracion completada"

echo "Iniciando aplicacion FastAPI"
exec uvicorn src.app.main:app --host 0.0.0.0 --port 8000
