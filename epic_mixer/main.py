import asyncio

from rich.console import Console

from .cli import gather_user_inputs, parse_args
from .core.orchestrator import orquestador_epico
from .core.wallets import derivar_wallets, generar_nuevo_mnemonic
from .core.web3_utils import esperar_deposito, setup_web3
from .utils.config import load_strategy
from .utils.reporting import exportar_reporte_encriptado

log = Console()


def run():
    """Punto de entrada principal para ejecutar el Epic Mixer."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        log.print("\n[bold orange]🛑 Operación interrumpida por el usuario.")
    except Exception as e:
        log.print(f"[bold red]❌ Ha ocurrido un error fatal: {e}")
        log.print_exception(show_locals=True)


async def async_main():
    """Función asíncrona principal que coordina la ejecución del script."""
    log.rule("[bold red]🌪️ Epic Mixer - Orquestador de Caos 🌪️[/bold red]")

    args = parse_args()
    config = load_strategy(args.strategy)
    config["network"] = args.network

    web3 = setup_web3(args.network)
    if not await web3.is_connected():
        log.print("[bold red]❌ No se pudo conectar al nodo. Abortando.")
        exit(1)

    session_mnemonic = generar_nuevo_mnemonic()

    # Derivar todas las wallets necesarias para la sesión
    num_estrategia_wallets = len(config.get("distribution", []))
    num_tormenta_wallets = config.get("wallets_in_storm", 20)

    wallets = {
        "deposito": derivar_wallets(session_mnemonic, 1, 0),
        "estrategia": derivar_wallets(session_mnemonic, num_estrategia_wallets, 1),
        "tormenta": derivar_wallets(
            session_mnemonic, num_tormenta_wallets, 1 + num_estrategia_wallets
        ),
    }

    monto_depositado = await esperar_deposito(web3, wallets["deposito"][0].address)
    if monto_depositado <= 0:
        exit(1)

    # Propagar el monto depositado hacia la configuración para cálculos basados en porcentaje
    config["deposit_amount_bnb"] = monto_depositado

    final_wallets, password = gather_user_inputs(config)

    log.rule("[bold blue]🚀 Iniciando Orquestación")

    # Ejecutar orquestador y capturar log de transacciones para advanced reporting
    tx_report = await orquestador_epico(web3, config, wallets, final_wallets)

    # Preparar y guardar el reporte final
    report_data = {
        "session_details": {
            "session_mnemonic": session_mnemonic,
            "deposit_address": wallets["deposito"][0].address,
            "amount_deposited_bnb": monto_depositado,
        },
        "strategy_used": config,
        "final_destination_wallets": final_wallets,
        "generated_wallets_details": {
            "strategy_leg_wallets": [w.address for w in wallets["estrategia"]],
            "storm_wallets": [w.address for w in wallets["tormenta"]],
        },
        # Datos avanzados de transacciones
        "tx_report": tx_report,
    }
    exportar_reporte_encriptado(report_data, password)

    log.print("[bold green]✨ Orquestación de mezcla finalizada con éxito.")
