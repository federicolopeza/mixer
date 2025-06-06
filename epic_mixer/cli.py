import argparse
import getpass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from .core.web3_utils import es_direccion_valida

log = Console()

def parse_args():
    """Parsea los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Epic Mixer: Un orquestador de ofuscación de transacciones en BSC.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-n", "--network", 
        type=str, 
        choices=['mainnet', 'testnet'], 
        default='testnet', 
        help="Red a utilizar (default: testnet)."
    )
    parser.add_argument(
        "--strategy", 
        type=str, 
        default="strategy.json", 
        help="Archivo de configuración de la estrategia (default: strategy.json)."
    )
    return parser.parse_args()

def gather_user_inputs(config: dict) -> tuple:
    """Recopila todas las entradas interactivas del usuario."""
    log.rule("[bold cyan]⚙️ Configuración de Destinos")
    
    # Pedir direcciones para las piernas de la estrategia que lo requieran
    for leg in config['distribution']:
        if leg['type'] == 'exchange':
            address = Prompt.ask(f"Introduce la dirección de depósito para la pierna '[bold yellow]{leg['name']}[/bold yellow]'")
            if not es_direccion_valida(address):
                log.print("[bold red]❌ Dirección inválida.")
                exit(1)
            leg['destination_address'] = address

    num_final_wallets = int(Prompt.ask("🔢 ¿A cuántas wallets finales quieres distribuir los fondos?", default="3"))
    if num_final_wallets <= 0:
        log.print("[bold red]❌ Debes especificar al menos una wallet final.")
        exit(1)

    final_wallets = []
    for i in range(num_final_wallets):
        address = Prompt.ask(f"  -> Dirección final {i+1}")
        if not es_direccion_valida(address):
            log.print("[bold red]❌ Dirección inválida.")
            exit(1)
        final_wallets.append(address)

    password = getpass.getpass("🔑 Introduce una contraseña para encriptar el reporte final: ")
    if not password:
        log.print("[bold red]❌ La contraseña no puede estar vacía.")
        exit(1)

    log.rule("[bold yellow]Confirmación Final")
    log.print(f"Estrategia: [cyan]{config['strategy_description']}[/cyan]")
    log.print(f"Wallets finales: {len(final_wallets)}")
    log.print(f"Red: [cyan]{config['network'].upper()}[/cyan]")

    if not Confirm.ask("[bold yellow]¿Iniciar la ejecución de la estrategia?", default=False):
        log.print("Operación cancelada.")
        exit(0)
    
    return final_wallets, password 