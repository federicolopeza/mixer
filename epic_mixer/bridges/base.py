from abc import ABC, abstractmethod

from rich.console import Console

console = Console()


class BaseBridgeAdapter(ABC):
    name: str = "base"

    @abstractmethod
    async def bridge(
        self,
        web3,
        source_wallet,
        amount_wei: int,
        to_chain: str,
        dest_address: str,
    ) -> str:
        """Realiza la operación de puente y devuelve un hash/reference."""
        raise NotImplementedError
