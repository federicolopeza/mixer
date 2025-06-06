import pytest

from epic_mixer.noise_generator import generate_noise


class DummyEth:
    async def get_balance(self, address):
        return 0


class DummyWeb3:
    eth = DummyEth()


@pytest.mark.asyncio
async def test_generate_noise_empty_wallets():
    web3 = DummyWeb3()
    wallets = {"estrategia": [], "tormenta": []}
    config = {}
    result = await generate_noise(web3, wallets, config)
    assert result is True
