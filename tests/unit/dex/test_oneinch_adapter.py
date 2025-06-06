import pytest

from epic_mixer.dex.oneinch_adapter import OneInchAdapter


@pytest.mark.asyncio
async def test_oneinch_adapter_returns_fake_hash():
    adapter = OneInchAdapter()
    DummyWallet = type("W", (), {"address": "0xdef456", "key": "0xkey"})
    wallet = DummyWallet()
    txh = await adapter.swap(None, wallet, 101112, ["TOKENA", "TOKENB"], 0.7)
    assert isinstance(txh, str)
    assert txh.startswith("0x")
    assert all(ch == "o" for ch in txh[2:])
