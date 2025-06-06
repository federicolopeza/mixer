from web3 import AsyncWeb3
from web3 import AsyncHTTPProvider
from aiohttp_socks import ProxyConnector
from rich.console import Console
from epic_mixer.core.web3_utils import RPC_URLS

console = Console()


def setup_web3_tor(network_mode: str) -> AsyncWeb3:
    """Configura AsyncWeb3 para enrutar todo el tráfico RPC a través de Tor (SOCKS5)."""
    rpc_url = RPC_URLS.get(network_mode)
    if not rpc_url:
        console.print(f"[bold red]❌ Red '{network_mode}' no válida para TorRPC.")
        raise ValueError(f"Red '{network_mode}' no válida.")

    # Configurar conector SOCKS5 apuntando al proxy Tor local
    connector = ProxyConnector.from_url("socks5://127.0.0.1:9050")
    provider = AsyncHTTPProvider(rpc_url, session_args={"connector": connector})
    web3 = AsyncWeb3(provider)
    console.print(f"[green]✅ Web3 TOR configurado para la red {network_mode.upper()}")
    return web3
