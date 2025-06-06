import json
from rich.console import Console

log = Console()

def load_strategy(strategy_file: str) -> dict:
    """Carga y valida el archivo de configuración de la estrategia."""
    try:
        with open(strategy_file) as f:
            config = json.load(f)
        # Adaptar configuraciones de versiones nuevas (por ejemplo, bloque "storm") a claves legacy
        if 'storm' in config and isinstance(config['storm'], dict):
            storm_cfg = config['storm']

            # Número de wallets utilizadas en la tormenta
            config.setdefault('wallets_in_storm', storm_cfg.get('wallets', 20))

            # Rondas de mezcla
            config.setdefault('mixing_rounds', storm_cfg.get('mixing_rounds', 15))

            # Cantidad de gas a fondear por wallet de tormenta (en BNB)
            config.setdefault('storm_wallet_gas_amount_bnb', storm_cfg.get('gas_amount_bnb', 0.002))

        # Validar el schema completo de la estrategia
        def is_addr(addr: str) -> bool:
            from epic_mixer.core.web3_utils import es_direccion_valida
            return es_direccion_valida(addr)

        # Validar bridges
        for b in config.get('bridges', []):
            if not all(k in b for k in ('name', 'from_chain', 'to_chain', 'amount_pct')):
                log.print(f"[bold red]❌ Bridge inválido: {b}")
                exit(1)
        # Validar dex_swaps
        for d in config.get('dex_swaps', []):
            if not all(k in d for k in ('chain', 'router', 'path', 'slippage')):
                log.print(f"[bold red]❌ DEX swap inválido: {d}")
                exit(1)
            if not isinstance(d['path'], list) or d['slippage'] < 0 or d['slippage'] > 1:
                log.print(f"[bold red]❌ Configuración DEX incorrecta: {d}")
                exit(1)
        # Validar ruido
        noise = config.get('noise_profile', {})
        if noise:
            n_txs = noise.get('n_micro_txs', {})
            if not (isinstance(n_txs.get('min',0), int) and isinstance(n_txs.get('max',0), int) and n_txs['min'] <= n_txs['max']):
                log.print(f"[bold red]❌ Noise profile inválido: {noise}")
                exit(1)
            for c in noise.get('contract_pool', []):
                # pueden ser direcciones o nombres de contrato
                pass
        # Validar time_windows
        tw = config.get('time_windows', {})
        if tw:
            ah = tw.get('active_hours', [])
            wb = tw.get('weekend_bias', 0)
            if not (isinstance(ah, list) and len(ah)==2 and all(isinstance(h,int) and 0<=h<24 for h in ah)):
                log.print(f"[bold red]❌ time_windows inválido: {tw}")
                exit(1)
            if not (isinstance(wb, (int,float)) and 0<=wb<=1):
                log.print(f"[bold red]❌ weekend_bias inválido: {wb}")
                exit(1)
        # Validar distribution
        for leg in config.get('distribution', []):
            if leg.get('type')=='exchange':
                addr = leg.get('destination_address')
                if not addr or not is_addr(addr):
                    log.print(f"[bold red]❌ Dirección de exchange inválida: {leg}")
                    exit(1)
            if not ('amount_bnb' in leg or 'amount_pct' in leg):
                log.print(f"[bold red]❌ Debe especificar amount_bnb o amount_pct en: {leg}")
                exit(1)
        log.print(f"[green]✅ Estrategia '{config.get('strategy_description', 'N/A')}' validada y cargada desde '{strategy_file}'.")
        return config
    except FileNotFoundError:
        log.print(f"[bold red]❌ Archivo de estrategia '{strategy_file}' no encontrado.")
        log.print("[bold yellow]Asegúrate de tener un archivo de estrategia (puedes copiar 'strategy.json.example' a 'strategy.json').")
        exit(1)
    except json.JSONDecodeError:
        log.print(f"[bold red]❌ Error al leer el archivo de estrategia '{strategy_file}'. Asegúrate de que es un JSON válido.")
        exit(1) 