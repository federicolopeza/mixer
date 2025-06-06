import pytest

from epic_mixer.failover import handle_failover


class DummyEth:
    async def chain_id(self):
        return 1

    async def gas_price(self):
        return 21000

    async def get_balance(self, address):
        return 100000


class DummyWeb3:
    eth = DummyEth()


@pytest.mark.asyncio
async def test_handle_failover_returns_true_for_empty_roles(monkeypatch):
    web3 = DummyWeb3()
    # Wallets sin estrategia ni tormenta, solo deposito
    DummyWallet = type("W", (), {"address": "0xabc", "key": "0xkey"})
    wallets = {"estrategia": [], "tormenta": [], "deposito": [DummyWallet()]}
    config = {}
    result = await handle_failover(web3, wallets, config)
    assert result is True
