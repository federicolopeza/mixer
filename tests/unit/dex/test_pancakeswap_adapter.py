import pytest
from epic_mixer.dex.pancakeswap_adapter import PancakeSwapAdapter

@pytest.mark.asyncio
async def test_pancakeswap_adapter_returns_fake_hash():
    adapter = PancakeSwapAdapter()
    DummyWallet = type("W", (), {"address": "0xabc123", "key": "0xkey"})
    wallet = DummyWallet()
    txh = await adapter.swap(None, wallet, 789, ["TOKEN1", "TOKEN2"], 0.5)
    assert isinstance(txh, str)
    assert txh.startswith("0x")
    assert all(ch == 'p' for ch in txh[2:]) 