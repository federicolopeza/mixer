import secrets

from apscheduler.schedulers.asyncio import AsyncIOScheduler

sr = secrets.SystemRandom()
from datetime import datetime, timedelta

from rich.console import Console

console = Console()


class MixerScheduler:
    """Scheduler para calendarizar fases del mixer con delays aleatorios."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        console.print("[green]✅ MixerScheduler iniciado.")

    def shutdown(self):
        """Detiene el scheduler."""
        self.scheduler.shutdown()
        console.print("[red]Scheduler detenido.")

    def schedule_phase(
        self,
        phase_name: str,
        func,
        args: list = None,
        min_delay_sec: int = 0,
        max_delay_sec: int = 0,
    ) -> datetime:
        """
        Programa la ejecución de `func` tras un delay aleatorio entre min_delay_sec y max_delay_sec.
        Devuelve la fecha y hora programada.
        """
        args = args or []
        delay = sr.uniform(min_delay_sec, max_delay_sec)
        run_time = datetime.now() + timedelta(seconds=delay)
        console.print(
            f"[yellow]⏱ Programando fase '{phase_name}' en {delay:.1f}s (ejecución: {run_time})."
        )
        self.scheduler.add_job(
            func,
            "date",
            run_date=run_time,
            args=args,
            id=phase_name,
            misfire_grace_time=60,
        )
        return run_time
