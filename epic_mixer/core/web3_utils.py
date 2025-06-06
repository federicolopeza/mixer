import asyncio
import time
from typing import Dict, Any

import qrcode
from rich.console import Console
from rich.spinner import Spinner
from web3 import Web3, AsyncWeb3
from web3 import AsyncHTTPProvider

log = Console()

# CONSTANTES
# GAS_LIMIT = 21000 # Eliminado para usar estimación dinámica
DEPOSIT_TIMEOUT_MINS = 30
RPC_URLS = {
    "testnet": "https://data-seed-prebsc-1-s1.binance.org:8545",
    "mainnet": "https://bsc-dataseed1.binance.org/",
}


def es_direccion_valida(address: str) -> bool:
    """Verifica si una dirección de Ethereum es válida."""
    return Web3.is_address(address)


def setup_web3(network_mode: str) -> AsyncWeb3:
    """Configura y retorna una instancia de AsyncWeb3."""
    rpc_url = RPC_URLS.get(network_mode)
    if not rpc_url:
        log.print(
            f"[bold red]❌ Red '{network_mode}' no válida. Usa 'testnet' o 'mainnet'."
        )
        exit(1)

    web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
    log.print(
        f"[bold green]✅ Proveedor Web3 configurado para la red {network_mode.upper()}"
    )
    return web3


async def esperar_deposito(web3: AsyncWeb3, deposit_address: str) -> float:
    """Espera a que se reciba un depósito en la dirección especificada."""
    log.rule(f"[bold yellow]Esperando depósito en la dirección")
    qr = qrcode.QRCode()
    qr.add_data(deposit_address)
    log.print("\n[bold]Escanea este QR o copia la dirección para enviar tus BNB[/bold]")
    qr.print_tty()
    log.print(f"\nDirección: [bold cyan]{deposit_address}[/bold cyan]")

    start_time = time.time()
    spinner = Spinner("dots", text=" Esperando transacción...")
    with log.status(spinner) as status:
        while True:
            try:
                balance_wei = await web3.eth.get_balance(deposit_address)
                if balance_wei > 0:
                    balance_bnb = Web3.from_wei(balance_wei, "ether")
                    log.print(
                        f"[bold green]✅ ¡Depósito detectado! Saldo: {balance_bnb:.6f} BNB"
                    )
                    return float(balance_bnb)

                elapsed_time = time.time() - start_time
                if elapsed_time > DEPOSIT_TIMEOUT_MINS * 60:
                    log.print(
                        f"[bold red]❌ Tiempo de espera agotado ({DEPOSIT_TIMEOUT_MINS} min)."
                    )
                    return 0.0

                remaining_time = DEPOSIT_TIMEOUT_MINS * 60 - elapsed_time
                status.update(
                    f" Esperando transacción... (tiempo restante: {int(remaining_time // 60)}m {int(remaining_time % 60)}s)"
                )
                await asyncio.sleep(10)
            except Exception as e:
                log.print(f"Error al consultar balance: {e}")
                await asyncio.sleep(15)


async def enviar_transaccion(
    web3: AsyncWeb3,
    tx_params: Dict[str, Any],
    sender_key: str,
    gas_price_multiplier: float = 1.0,
    nonce: int = None,
):
    """Firma y envía una única transacción, manejando errores y gas dinámico."""
    try:
        # 1. Asignar 'from' si no está presente
        if "from" not in tx_params:
            account = web3.eth.account.from_key(sender_key)
            tx_params["from"] = account.address

        # 2. Gestionar Nonce
        if nonce is None:
            tx_params["nonce"] = await web3.eth.get_transaction_count(tx_params["from"])
        else:
            tx_params["nonce"] = nonce

        # 3. Gestionar Precio del Gas (con aleatorización)
        if "gasPrice" not in tx_params:
            base_gas_price = await web3.eth.gas_price
            tx_params["gasPrice"] = int(base_gas_price * gas_price_multiplier)

        # 4. Estimar Gas si no se provee
        if "gas" not in tx_params:
            tx_params["gas"] = await web3.eth.estimate_gas(tx_params)

        signed_tx = web3.eth.account.sign_transaction(tx_params, sender_key)
        tx_hash = await web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # Esperar el recibo para confirmar la transacción
        receipt = await web3.eth.wait_for_transaction_receipt(tx_hash)

        if receipt.status == 1:
            log.print(
                f"[grey50]TX exitosa desde {tx_params['from'][:10]}... a {tx_params['to'][:10]}... Hash: {tx_hash.hex()}",
                highlight=False,
            )
        else:
            log.print(
                f"[bold red]❌ La transacción falló (revertida) desde {tx_params['from'][:10]}. Hash: {tx_hash.hex()}"
            )

        return tx_hash, receipt

    except Exception as e:
        log.print(
            f"[bold red]❌ Error en TX desde {tx_params.get('from', 'N/A')[:10]}: {e}"
        )
        return None, None
