import pytest
from epic_mixer.bridges.stargate_adapter import StargateAdapter


@pytest.mark.asyncio
async def test_stargate_adapter_returns_fake_hash():
    adapter = StargateAdapter()
    DummyWallet = type("W", (), {"address": "0xdef456", "key": "0xkey"})
    wallet = DummyWallet()
    txh = await adapter.bridge(None, wallet, 456, "arbitrum", "0xdest")
    assert isinstance(txh, str)
    assert txh.startswith("0x")
    assert all(ch == "s" for ch in txh[2:])
