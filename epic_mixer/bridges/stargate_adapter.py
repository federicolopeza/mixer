from .base import BaseBridgeAdapter
from web3 import AsyncWeb3
from rich.console import Console
import aiohttp

console = Console()


class StargateAdapter(BaseBridgeAdapter):
    name = "stargate"

    async def bridge(
        self,
        web3: AsyncWeb3,
        source_wallet,
        amount_wei: int,
        to_chain: str,
        dest_address: str,
    ) -> str:
        """Inicia un puente cross-chain usando Stargate (LayerZero)."""
        console.print(
            f"[magenta]🔗 Iniciando puente Stargate: {amount_wei} wei de {source_wallet.address} a {dest_address} en {to_chain}."
        )
        # TODO: Implementar integración con la API de Stargate
        async with aiohttp.ClientSession() as session:
            # payload = {...}
            # response = await session.post(STARGATE_API_URL, json=payload)
            # data = await response.json()
            pass
        fake_hash = "0x" + "s" * 64
        console.print(f"[green]✅ Puente Stargate simulado. Ref: {fake_hash}")
        return fake_hash
