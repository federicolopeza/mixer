import asyncio
import secrets
from web3 import Web3, AsyncWeb3
from rich.console import Console
from epic_mixer.core.web3_utils import enviar_transaccion

console = Console()
sr = secrets.SystemRandom()


async def generate_noise(web3: AsyncWeb3, wallets: dict, config: dict):
    """Ejecuta transacciones de ruido para camuflar actividad en las wallets."""
    noise_cfg = config.get("noise_profile", {})
    n_cfg = noise_cfg.get("n_micro_txs", {})
    min_txs = n_cfg.get("min", 1)
    max_txs = n_cfg.get("max", 1)
    contract_pool = noise_cfg.get("contract_pool", [])

    total_txs = sr.randint(min_txs, max_txs)
    console.print(
        f"[yellow]🔊 Generando {total_txs} transacciones de ruido (micro-txs)."
    )

    # Combinar todas las wallets disponibles (estrategia + tormenta)
    all_wallets = wallets.get("estrategia", []) + wallets.get("tormenta", [])
    if not all_wallets:
        console.print(
            "[yellow]⚠️ No hay wallets disponibles para generar ruido. Omitiendo ruido."
        )
        return True
    tasks = []

    for i in range(total_txs):
        # Seleccionar wallet y contratante aleatorio
        w = sr.choice(all_wallets)
        if contract_pool:
            dest = sr.choice(contract_pool)
            value_wei = Web3.to_wei(sr.uniform(0.000001, 0.00001), "ether")
            tx_params = {"to": dest, "value": int(value_wei)}
        else:
            # Enviar micropago a otra wallet para ruido interno
            dest_wallet = sr.choice(all_wallets)
            while dest_wallet.address == w.address:
                dest_wallet = sr.choice(all_wallets)
            value_wei = Web3.to_wei(sr.uniform(0.000001, 0.00001), "ether")
            tx_params = {"to": dest_wallet.address, "value": int(value_wei)}

        tasks.append(enviar_transaccion(web3, tx_params, w.key))
        await asyncio.sleep(sr.uniform(1, 3))

    # Ejecutar todos los envíos
    if tasks:
        await asyncio.gather(*tasks)
    console.print(f"[green]✅ Ruido completado.")
    return True
