from importlib import import_module

DEX_ADAPTERS = {
    'pancakeswap': 'epic_mixer.dex.pancakeswap_adapter.PancakeSwapAdapter',
    '1inch': 'epic_mixer.dex.oneinch_adapter.OneInchAdapter',
}


def get_dex_adapter(name: str):
    """Devuelve una instancia del adaptador de DEX solicitado."""
    path = DEX_ADAPTERS.get(name.lower())
    if not path:
        raise ValueError(f"DEX '{name}' no soportado.")
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    adapter_cls = getattr(module, class_name)
    return adapter_cls() 