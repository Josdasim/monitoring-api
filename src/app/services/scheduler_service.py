from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from src.app.config.database import sessionLocal
from src.app.services.health_check_runner import HealthCheckRunner
import atexit


class HealthCheckScheduler:
    """Ejecuta health checks periodicos"""
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        print("Se ha iniciado el planificador...")

        # Al terminar acaba el proceso de scheduler
        atexit.register(lambda: self.scheduler.shutdown())

    def start_monitoring(self, interval_seconds: int = 60):
        """Inicia el monitoreo periodico de todos los servicios
            Args:
                interval_seconds: Cada cuantos segundos verificara (default: 60)
        """
        def check_all():
            """Funcion que se ejecuta en cada intervalo"""
            db: Session = sessionLocal()
            try:
                HealthCheckRunner.check_all_active_services(db)
            except Exception as e:
                print("Error en el scheduler: {e}")

        self.scheduler.add_job(
            func = check_all,
            trigger = IntervalTrigger(seconds = interval_seconds),
            id = "health_check_job",
            name = "Revisar estado de todos los servicios",
            replace_existing = True
        )

        print(f"Monitoreo programado para cada {interval_seconds} segundos")

        # Para comenzar con el primero sin necesidad de llegar al primer intervalo
        check_all()

    def stop_monitoring(self):
        """Detiene el monitoreo"""
        if self.scheduler.get_job("health_check_job"):
            self.scheduler.remove_job("health_check_job")
            print("Monitoreo detenido")


# Intancia grobal del schedule, se crea una unica vez
health_scheduler = HealthCheckScheduler()