import datetime
from rich.console import Console
from .encryption import encrypt_data

log = Console()

def exportar_reporte_encriptado(report_data: dict, password: str):
    """Exporta el reporte de sesión en un archivo encriptado."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mixer_report_encrypted_{timestamp}.dat"
    
    try:
        encrypted_data = encrypt_data(report_data, password)
        with open(filename, "wb") as f:
            f.write(encrypted_data)
        log.print(f"[bold blue]\n📁 Reporte de sesión encriptado guardado en {filename}")
        log.print("[bold yellow]¡Guarda este archivo y tu contraseña! ¡No hay forma de recuperarlos!")
    except Exception as e:
        log.print(f"[bold red]❌ Error al crear el reporte encriptado: {e}") 