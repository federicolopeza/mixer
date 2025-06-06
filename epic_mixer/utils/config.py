import json
from rich.console import Console
from pydantic import BaseModel, Field, conlist, confloat, validator, root_validator, ValidationError
from typing import List, Optional, Dict

log = Console()

class BridgeConfig(BaseModel):
    name: str
    from_chain: str
    to_chain: str
    amount_pct: confloat(ge=0, le=1)

class DexSwapConfig(BaseModel):
    chain: str
    router: str
    path: List[str]
    slippage: confloat(ge=0, le=1)

class NoiseProfileConfig(BaseModel):
    n_micro_txs: Dict[str, int]
    contract_pool: List[str] = []

    @validator('n_micro_txs')
    def check_n_micro_txs(cls, v):
        if not (v.get('min') is not None and v.get('max') is not None and v['min'] <= v['max']):
            raise ValueError('n_micro_txs must have min <= max')
        return v

class TimeWindowsConfig(BaseModel):
    active_hours: conlist(int, min_items=2, max_items=2)
    weekend_bias: confloat(ge=0, le=1)

class DistributionConfig(BaseModel):
    type: str
    destination_address: Optional[str]
    amount_bnb: Optional[float]
    amount_pct: Optional[float]

    @root_validator
    def check_amount(cls, values):
        if values.get('amount_bnb') is None and values.get('amount_pct') is None:
            raise ValueError('Must specify amount_bnb or amount_pct')
        return values

class StrategyConfig(BaseModel):
    strategy_description: Optional[str]
    bridges: List[BridgeConfig] = []
    dex_swaps: List[DexSwapConfig] = []
    noise_profile: Optional[NoiseProfileConfig]
    time_windows: Optional[TimeWindowsConfig]
    distribution: List[DistributionConfig] = []
    wallets_in_storm: int = 20
    mixing_rounds: int = 15
    storm_wallet_gas_amount_bnb: float = 0.002

    class Config:
        extra = 'allow'

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

        # Validar con Pydantic
        try:
            cfg = StrategyConfig.parse_obj(config)
        except ValidationError as e:
            log.print(f"[bold red]❌ Error en validación de estrategia:\n{e}")
            exit(1)
        log.print(f"[green]✅ Estrategia '{cfg.strategy_description or 'N/A'}' validada y cargada.")
        return cfg.dict()
    except FileNotFoundError:
        log.print(f"[bold red]❌ Archivo de estrategia '{strategy_file}' no encontrado.")
        log.print("[bold yellow]Asegúrate de tener un archivo de estrategia (puedes copiar 'strategy.json.example' a 'strategy.json').")
        exit(1)
    except json.JSONDecodeError:
        log.print(f"[bold red]❌ Error al leer el archivo de estrategia '{strategy_file}'. Asegúrate de que es un JSON válido.")
        exit(1) 