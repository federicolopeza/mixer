import json
from rich.console import Console

log = Console()

def load_strategy(strategy_file: str) -> dict:
    """Carga y valida el archivo de configuración de la estrategia."""
    try:
        with open(strategy_file) as f:
            config = json.load(f)
        log.print(f"[green]✅ Estrategia '{config.get('strategy_description', 'N/A')}' cargada desde '{strategy_file}'.")
        # Aquí se podrían añadir más validaciones del schema de la estrategia
        return config
    except FileNotFoundError:
        log.print(f"[bold red]❌ Archivo de estrategia '{strategy_file}' no encontrado.")
        log.print("[bold yellow]Asegúrate de tener un archivo de estrategia (puedes copiar 'strategy.json.example' a 'strategy.json').")
        exit(1)
    except json.JSONDecodeError:
        log.print(f"[bold red]❌ Error al leer el archivo de estrategia '{strategy_file}'. Asegúrate de que es un JSON válido.")
        exit(1) 