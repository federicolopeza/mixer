import asyncio
import random
from typing import Dict, List, Any
from rich.console import Console
from web3 import Web3, AsyncWeb3
from .web3_utils import enviar_transaccion, GAS_LIMIT

log = Console()

async def orquestador_epico(web3: AsyncWeb3, config: Dict, wallets: Dict, final_wallets: List[str]):
    """Orquesta la estrategia de mezcla épica definida en la configuración."""
    gas_price = await web3.eth.gas_price
    wallet_deposito = wallets['deposito'][0]
    # wallets_tormenta = wallets['tormenta'] # Preparado para una futura implementación de tormenta
    chain_id = await web3.eth.chain_id
    
    # FASE 1: Dispersión Estratégica
    log.rule("[bold cyan]🔀 1. Dispersión Estratégica")
    tasks = []
    nonce_inicial = await web3.eth.get_transaction_count(wallet_deposito.address)
    
    for i, leg in enumerate(config['distribution']):
        sub_wallet = wallets['estrategia'][i]
        monto_wei = Web3.to_wei(leg['amount_bnb'], 'ether')
        
        tx_params = {
            'from': wallet_deposito.address, 'to': sub_wallet.address, 'value': monto_wei,
            'gas': GAS_LIMIT, 'gasPrice': gas_price, 'nonce': nonce_inicial + i, 'chainId': chain_id
        }
        tasks.append(enviar_transaccion(web3, tx_params, wallet_deposito.key))
        log.print(f"Programando envío de {leg['amount_bnb']} BNB a sub-wallet para la pierna '{leg['name']}'")

    await asyncio.gather(*tasks)
    log.print("[green]Dispersión estratégica completada.")
    await asyncio.sleep(5)

    # FASE 2: Tormenta de Mezcla
    log.rule(f"[bold magenta]🔄 2. Ejecutando Tormenta de Mezcla ({config['mixing_rounds']} rondas)")
    log.print("Iniciando rondas de transacciones caóticas entre las wallets de la tormenta...")
    # Lógica de tormenta (simplificada para este ejemplo, puede ser expandida)
    # Fondos de las sub-wallets se mueven a las wallets de tormenta para mezclarse.
    # Por ahora, simulamos el tiempo que tomaría
    await asyncio.sleep(config['mixing_rounds'] * 2) 
    log.print("[cyan]Tormenta de mezcla simulada completada.")


    # FASE 3: Ejecución de Piernas de la Estrategia
    log.rule("[bold blue]🚀 3. Ejecutando Estrategia de Distribución")
    for i, leg in enumerate(config['distribution']):
        sub_wallet = wallets['estrategia'][i]
        log.print(f"--- Ejecutando pierna: [bold yellow]{leg['name']}[/bold yellow] ---")
        
        balance = await web3.eth.get_balance(sub_wallet.address)
        if balance <= gas_price * GAS_LIMIT:
            log.print(f"[yellow]Saldo insuficiente en sub-wallet para '{leg['name']}'. Saltando.")
            continue
            
        nonce = await web3.eth.get_transaction_count(sub_wallet.address)
        
        if leg['type'] == 'exchange':
            destino = leg['destination_address']
            tx_value = balance - (gas_price * GAS_LIMIT)
            tx_params = {
                'from': sub_wallet.address, 'to': destino, 'value': tx_value,
                'gas': GAS_LIMIT, 'gasPrice': gas_price, 'nonce': nonce, 'chainId': chain_id
            }
            await enviar_transaccion(web3, tx_params, sub_wallet.key)
            log.print(f"Enviados {Web3.from_wei(tx_value, 'ether'):.4f} BNB a Exchange: {destino[:15]}...")
        
        elif leg['type'] in ['privacy_pool', 'direct_distribution']:
            destino = random.choice(final_wallets)
            tx_value = balance - (gas_price * GAS_LIMIT)
            tx_params = {
                'from': sub_wallet.address, 'to': destino, 'value': tx_value,
                'gas': GAS_LIMIT, 'gasPrice': gas_price, 'nonce': nonce, 'chainId': chain_id
            }
            await enviar_transaccion(web3, tx_params, sub_wallet.key)
            log.print(f"Distribuidos {Web3.from_wei(tx_value, 'ether'):.4f} BNB a wallet final: {destino[:15]}...")
        
        await asyncio.sleep(random.uniform(3, 8)) 