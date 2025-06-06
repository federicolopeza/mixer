import pytest
from epic_mixer.scheduler import MixerScheduler
from datetime import datetime

@pytest.mark.asyncio
async def test_schedule_phase_and_shutdown():
    scheduler = MixerScheduler()
    # Función dummy
    def dummy_task():
        pass
    # Programar tarea con delay 0-1 segundos
    run_time = scheduler.schedule_phase("test_phase", dummy_task, [], min_delay_sec=0, max_delay_sec=1)
    assert isinstance(run_time, datetime)
    assert run_time >= datetime.now()

    # Apagar scheduler
    scheduler.shutdown() 