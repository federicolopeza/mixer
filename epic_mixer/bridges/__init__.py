from importlib import import_module

BRIDGE_ADAPTERS = {
    "cbridge": "epic_mixer.bridges.cbridge_adapter.CBridgeAdapter",
    "stargate": "epic_mixer.bridges.stargate_adapter.StargateAdapter",
}


def get_bridge_adapter(name: str):
    """Devuelve una instancia del adaptador de puente solicitado."""
    path = BRIDGE_ADAPTERS.get(name.lower())
    if not path:
        raise ValueError(f"Bridge '{name}' no soportado.")
    module_path, class_name = path.rsplit(".", 1)
    module = import_module(module_path)
    adapter_cls = getattr(module, class_name)
    return adapter_cls()
