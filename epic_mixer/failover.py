import asyncio
from web3 import Web3, AsyncWeb3
from rich.console import Console
from epic_mixer.core.web3_utils import enviar_transaccion

console = Console()

async def handle_failover(web3: AsyncWeb3, wallets: dict, config: dict):
    """Recupera fondos de todas las wallets en caso de fallo crítico, enviándolos a la vault."""
    vault = config.get('emergency_vault_address')
    if not vault:
        vault = None
    if wallets.get('deposito'):
        vault = wallets['deposito'][0].address

    console.print(f"[bold red]❗ Fallo crítico. Iniciando failover hacia vault: {vault}")
    tasks = []
    # Obtener parámetros de la red
    chain_id = await web3.eth.chain_id()
    gas_price = await web3.eth.gas_price()
    min_gas = gas_price * 21000

    # Colección de todas las wallets de estrategia y tormenta
    for role in ['estrategia', 'tormenta']:
        for w in wallets.get(role, []):
            try:
                balance = await web3.eth.get_balance(w.address)
                if balance > min_gas:
                    send_value = balance - min_gas
                    tx_params = {'to': vault, 'value': send_value, 'chainId': chain_id}
                    tasks.append(enviar_transaccion(web3, tx_params, w.key))
            except Exception as e:
                console.print(f"[bold red]Error al recuperar fondos de {w.address}: {e}")

    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    console.print("[green]✅ Failover completado.")
    return True 