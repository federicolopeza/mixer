import asyncio
import random
import secrets

sr = secrets.SystemRandom()
from typing import Any, Dict, List

from rich.console import Console
from web3 import AsyncWeb3, Web3

from epic_mixer.bridges import get_bridge_adapter
from epic_mixer.dex import get_dex_adapter
from epic_mixer.failover import handle_failover
from epic_mixer.noise_generator import generate_noise
from epic_mixer.utils.advanced_reporting import generate_merkle_root

from .web3_utils import enviar_transaccion

log = Console()


async def _ejecutar_tormenta_de_mezcla(
    web3: AsyncWeb3, config: Dict[str, Any], wallets: Dict[str, Any]
) -> None:
    """Ejecuta la tormenta de transacciones entre las wallets de tormenta."""
    log.rule(
        f"[bold magenta]🌪️ 2. Ejecutando Tormenta de Mezcla ({config['mixing_rounds']} rondas)"
    )
    wallets_tormenta = wallets["tormenta"]

    # 1. Mover fondos de wallets de estrategia a wallets de tormenta para iniciar.
    log.print("Movilizando fondos hacia el pool de la tormenta...")
    tasks = []
    for i, wallet_estrategia in enumerate(wallets["estrategia"]):
        balance = await web3.eth.get_balance(wallet_estrategia.address)
        if balance > 0:
            # Distribuye a una wallet de tormenta aleatoria
            wallet_tormenta_destino = sr.choice(wallets_tormenta)
            tx_params = {"to": wallet_tormenta_destino.address, "value": balance}
            tasks.append(enviar_transaccion(web3, tx_params, wallet_estrategia.key))

    await asyncio.gather(*tasks)
    log.print("[green]Fondos movilizados para la tormenta.")
    await asyncio.sleep(3)

    # 2. Ejecutar rondas de mezcla caótica.
    for round_num in range(config["mixing_rounds"]):
        log.print(f"-> Ronda de tormenta {round_num + 1}/{config['mixing_rounds']}")

        wallets_con_fondos = []
        for w in wallets_tormenta:
            if await web3.eth.get_balance(w.address) > Web3.to_wei("0.001", "ether"):
                wallets_con_fondos.append(w)

        if len(wallets_con_fondos) < 2:
            log.print(
                "[yellow]No hay suficientes wallets con fondos para continuar la tormenta."
            )
            break

        origen = sr.choice(wallets_con_fondos)
        destino = sr.choice(
            [w for w in wallets_con_fondos if w.address != origen.address]
        )

        balance_origen_wei = await web3.eth.get_balance(origen.address)
        # Dejar algo de gas, enviar un % aleatorio del resto
        gas_fee_estimada = Web3.to_wei("0.001", "ether")
        monto_a_enviar_wei = int(
            (balance_origen_wei - gas_fee_estimada) * sr.uniform(0.2, 0.7)
        )

        if monto_a_enviar_wei > 0:
            tx_params = {"to": destino.address, "value": monto_a_enviar_wei}
            await enviar_transaccion(
                web3, tx_params, origen.key, gas_price_multiplier=sr.uniform(1.0, 1.05)
            )

        await asyncio.sleep(sr.uniform(2, 5))

    log.print("[green]✅ Tormenta de mezcla completada.")

    # 3. Consolidar fondos de vuelta a las wallets de estrategia.
    log.print(
        "Consolidando fondos de la tormenta de vuelta a las wallets de estrategia..."
    )
    tasks = []
    for i, wallet_tormenta in enumerate(wallets_tormenta):
        balance = await web3.eth.get_balance(wallet_tormenta.address)
        if balance > Web3.to_wei("0.001", "ether"):
            wallet_estrategia_destino = wallets["estrategia"][
                i % len(wallets["estrategia"])
            ]
            gas_fee_estimada = Web3.to_wei("0.001", "ether")
            tx_value = balance - gas_fee_estimada
            if tx_value > 0:
                tx_params = {"to": wallet_estrategia_destino.address, "value": tx_value}
                tasks.append(enviar_transaccion(web3, tx_params, wallet_tormenta.key))

    await asyncio.gather(*tasks)
    log.print("[green]Fondos consolidados.")


async def orquestador_epico(
    web3: AsyncWeb3,
    config: Dict[str, Any],
    wallets: Dict[str, Any],
    final_wallets: List[str],
) -> Dict[str, Any]:
    """Orquesta la estrategia de mezcla épica definida en la configuración."""
    # Iniciar orquestador con manejo de fallos
    gas_price = await web3.eth.gas_price
    try:
        # Ruido antes de la fase de financiación
        log.rule("[bold magenta]🔊 Ruido Pre-Mezcla")
        await generate_noise(web3, wallets, config)

        # Variables principales
        wallet_deposito = wallets["deposito"][0]
        wallets_estrategia = wallets["estrategia"]
        wallets_tormenta = wallets["tormenta"]
        chain_id = await web3.eth.chain_id
        gas_price = await web3.eth.gas_price
        # PRE-FASE: Fondear wallets de tormenta para el gas
        log.rule("[bold yellow]⛽ Pre-Fase: Fondeando Wallets de Tormenta para Gas")
        gas_para_tormenta = Web3.to_wei(
            config.get("storm_wallet_gas_amount_bnb", 0.002), "ether"
        )
        tasks = []
        nonce = await web3.eth.get_transaction_count(wallet_deposito.address)
        for i, wallet in enumerate(wallets_tormenta):
            tx_params = {
                "to": wallet.address,
                "value": gas_para_tormenta,
                "chainId": chain_id,
            }
            tasks.append(
                enviar_transaccion(
                    web3, tx_params, wallet_deposito.key, nonce=nonce + i
                )
            )
        await asyncio.gather(*tasks)
        log.print(
            f"[green]Wallets de tormenta fondeadas con {Web3.from_wei(gas_para_tormenta, 'ether')} BNB cada una."
        )
        await asyncio.sleep(3)

        # FASE 1: Financiación en Cadena
        log.rule("[bold cyan]🔗 1. Financiación Estratégica en Cadena")

        # La primera wallet de estrategia se fondea desde la wallet de depósito
        wallet_anterior = wallet_deposito

        # Calcular el monto total depositado si está disponible (para porcentajes)
        deposito_total_bnb = config.get("deposit_amount_bnb")

        for i, leg in enumerate(config["distribution"]):
            wallet_actual = wallets_estrategia[i]

            # Compatibilidad: admitir 'amount_bnb' o 'amount_pct'
            if "amount_bnb" in leg:
                monto_wei = Web3.to_wei(leg["amount_bnb"], "ether")
            elif "amount_pct" in leg and deposito_total_bnb is not None:
                monto_bnb_calc = (leg["amount_pct"] / 100) * deposito_total_bnb
                monto_wei = Web3.to_wei(monto_bnb_calc, "ether")
            else:
                log.print(
                    f"[red]❌ Pierna de estrategia sin 'amount_bnb' ni 'amount_pct'. Abortando pierna {leg.get('name', i)}."
                )
                continue

            # Mensaje descriptivo
            if "amount_bnb" in leg:
                descrip_monto = f"{leg['amount_bnb']} BNB"
            else:
                descrip_monto = f"{leg['amount_pct']}% (~{Web3.from_wei(monto_wei, 'ether'):.4f} BNB)"

            log.print(
                f"Financiando {descrip_monto} desde {wallet_anterior.address[:10]}... a {wallet_actual.address[:10]}..."
            )

            tx_params = {
                "to": wallet_actual.address,
                "value": monto_wei,
                "chainId": chain_id,
            }
            await enviar_transaccion(
                web3,
                tx_params,
                wallet_anterior.key,
                gas_price_multiplier=sr.uniform(1.0, 1.05),
            )

            wallet_anterior = wallet_actual
            await asyncio.sleep(sr.uniform(3, 8))  # Pausa entre eslabones de la cadena

        log.print("[green]Financiación en cadena completada.")
        await asyncio.sleep(5)

        # FASE 2: Tormenta de Mezcla Real
        await _ejecutar_tormenta_de_mezcla(web3, config, wallets)
        await asyncio.sleep(5)

        # FASE 2.5: Puentes Cross-Chain
        log.rule("[bold cyan]🔀 4. Puentes Cross-Chain")
        bridge_hashes = []
        deposito_bnb = config.get("deposit_amount_bnb")
        if deposito_bnb and config.get("bridges"):
            for b in config["bridges"]:
                adapter = get_bridge_adapter(b["name"])
                pct = b.get("amount_pct", 0)
                amt_bnb = (pct / 100) * deposito_bnb
                amt_wei = Web3.to_wei(amt_bnb, "ether")
                dest = final_wallets[0] if final_wallets else wallet_deposito.address
                txh = await adapter.bridge(
                    web3, wallet_deposito, amt_wei, b.get("to_chain"), dest
                )
                bridge_hashes.append(txh)
                await asyncio.sleep(sr.uniform(3, 8))
        log.print(f"[green]✅ Puentes ejecutados: {len(bridge_hashes)}")
        await asyncio.sleep(3)

        # FASE 2.6: Swaps en DEX
        log.rule("[bold cyan]🔄 5. Swaps en DEX")
        dex_hashes = []
        dex_cfgs = config.get("dex_swaps", [])
        if dex_cfgs and deposito_bnb:
            deposit_wei = Web3.to_wei(deposito_bnb, "ether")
            per_swap = int(deposit_wei / len(dex_cfgs))
            for d in dex_cfgs:
                adapter = get_dex_adapter(d["router"])
                path = d.get("path", [])
                slip = d.get("slippage", 0.005)
                txh = await adapter.swap(web3, wallet_deposito, per_swap, path, slip)
                dex_hashes.append(txh)
                await asyncio.sleep(sr.uniform(3, 8))
        log.print(f"[green]✅ Swaps DEX completados: {len(dex_hashes)}")
        await asyncio.sleep(3)

        # FASE 3: Ejecución de Piernas de la Estrategia
        log.rule("[bold blue]🚀 3. Ejecutando Estrategia de Distribución Final")
        for i, leg in enumerate(config["distribution"]):
            sub_wallet = wallets_estrategia[i]
            log.print(
                f"--- Ejecutando pierna: [bold yellow]{leg['name']}[/bold yellow] ---"
            )

            balance = await web3.eth.get_balance(sub_wallet.address)
            if balance <= gas_price * 21000:  # Usar una estimación segura
                log.print(
                    f"[yellow]Saldo insuficiente en sub-wallet para '{leg['name']}'. Saltando."
                )
                continue

            if leg["type"] == "exchange":
                destino = leg["destination_address"]
                tx_value = balance - (gas_price * 30000)  # Dejar un poco más para gas
                tx_params = {"to": destino, "value": tx_value, "chainId": chain_id}
                await enviar_transaccion(
                    web3,
                    tx_params,
                    sub_wallet.key,
                    gas_price_multiplier=sr.uniform(1.0, 1.05),
                )
                log.print(
                    f"Enviados {Web3.from_wei(tx_value, 'ether'):.4f} BNB a Exchange: {destino[:15]}..."
                )

            elif leg["type"] in ["privacy_pool", "direct_distribution"]:
                destino = random.choice(final_wallets)
                tx_value = balance - (gas_price * 30000)
                tx_params = {"to": destino, "value": tx_value, "chainId": chain_id}
                await enviar_transaccion(
                    web3,
                    tx_params,
                    sub_wallet.key,
                    gas_price_multiplier=sr.uniform(1.0, 1.05),
                )
                log.print(
                    f"Distribuidos {Web3.from_wei(tx_value, 'ether'):.4f} BNB a wallet final: {destino[:15]}..."
                )

            await asyncio.sleep(sr.uniform(3, 8))
            # Fin de la orquestación exitosa
            log.print("[bold green]✨ Orquestación completada sin errores.")
            # Generación de Merkle root para advanced reporting
            all_hashes = bridge_hashes + dex_hashes
            merkle_root = generate_merkle_root(all_hashes)
            return {
                "bridges": bridge_hashes,
                "dex": dex_hashes,
                "merkle_root": merkle_root,
            }
    except Exception as e:
        log.print(f"[bold red]❌ Error crítico en orquestador: {e}")
        # Mecanismo de recuperación segura
        await handle_failover(web3, wallets, config)
        raise
