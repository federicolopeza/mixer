import json
import argparse
import pytest
from unittest.mock import AsyncMock, MagicMock

from epic_mixer.main import run


class DummyWeb3:
    def __init__(self):
        self.eth = MagicMock()
        self.eth.get_balance = AsyncMock(return_value=0)
        self.eth.gas_price = AsyncMock(return_value=0)
        self.eth.get_transaction_count = AsyncMock(return_value=0)
        self.eth.chain_id = AsyncMock(return_value=1)

    async def is_connected(self):
        return True


@pytest.fixture(autouse=True)
def stub_dependencies(monkeypatch, tmp_path):
    # Crear archivo de estrategia mínimo
    strategy_path = tmp_path / "strategy.json"
    strategy = {"strategy_description": "E2E Test", "distribution": []}
    strategy_path.write_text(json.dumps(strategy))

    # Stub parse_args para usar nuestro strategy file
    args = argparse.Namespace(network="testnet", strategy=str(strategy_path))
    monkeypatch.setattr("epic_mixer.main.parse_args", lambda: args)

    # Stub setup_web3 y esperar_deposito
    web3_stub = DummyWeb3()
    monkeypatch.setattr(
        "epic_mixer.core.web3_utils.setup_web3", lambda network: web3_stub
    )
    monkeypatch.setattr(
        "epic_mixer.core.web3_utils.esperar_deposito", AsyncMock(return_value=1)
    )

    # Stub wallets
    class W:
        def __init__(self, addr):
            self.address = addr
            self.key = "key"

    monkeypatch.setattr(
        "epic_mixer.core.wallets.generar_nuevo_mnemonic", lambda: "seed"
    )
    monkeypatch.setattr(
        "epic_mixer.core.wallets.derivar_wallets",
        lambda seed, n, idx: [W(f"0x{i}") for i in range(n)],
    )

    # Stub orquestador_epico y exportar_reporte_encriptado
    monkeypatch.setattr(
        "epic_mixer.core.orchestrator.orquestador_epico", AsyncMock(return_value={})
    )
    monkeypatch.setattr(
        "epic_mixer.utils.reporting.exportar_reporte_encriptado", lambda data, pwd: None
    )

    # Usar variable de entorno para contraseña
    monkeypatch.setenv("MIXER_PASSWORD", "testpwd")


def test_run_mixer_e2e():
    # Ejecutar la función principal, no debería lanzar excepción
    run()
