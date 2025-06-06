import pytest

from epic_mixer.bridges.cbridge_adapter import CBridgeAdapter


@pytest.mark.asyncio
async def test_cbridge_adapter_returns_fake_hash():
    adapter = CBridgeAdapter()
    # Dummy wallet con dirección y clave arbitrarias
    DummyWallet = type("W", (), {"address": "0xabc123", "key": "0xkey"})
    wallet = DummyWallet()
    # Llamar al método bridge stub
    txh = await adapter.bridge(None, wallet, 123, "polygon", "0xdest")
    assert isinstance(txh, str)
    assert txh.startswith("0x")
    # Verificar que el hash está compuesto por 'c'
    assert all(ch == "c" for ch in txh[2:])
