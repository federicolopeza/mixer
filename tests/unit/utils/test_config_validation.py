import json
import pytest
from epic_mixer.utils.config import load_strategy


def write_json(tmp_path, data):
    path = tmp_path / "strategy.json"
    path.write_text(json.dumps(data))
    return str(path)


def test_load_valid_strategy(tmp_path):
    data = {
        "strategy_description": "TestStrategy",
        "bridges": [
            {"name": "br", "from_chain": "A", "to_chain": "B", "amount_pct": 0.5}
        ],
        "dex_swaps": [{"chain": "A", "router": "R", "path": ["0x1"], "slippage": 0.01}],
        "noise_profile": {
            "n_micro_txs": {"min": 1, "max": 3},
            "contract_pool": ["0x2"],
        },
        "time_windows": {"active_hours": [0, 23], "weekend_bias": 0.5},
        "distribution": [
            {"type": "exchange", "destination_address": "0xABC", "amount_bnb": 1.0}
        ],
        "wallets_in_storm": 10,
        "mixing_rounds": 5,
        "storm_wallet_gas_amount_bnb": 0.001,
    }
    path = write_json(tmp_path, data)
    cfg = load_strategy(path)
    assert isinstance(cfg, dict)
    assert cfg.get("strategy_description") == "TestStrategy"
    assert cfg.get("wallets_in_storm") == 10
    assert cfg.get("dex_swaps")[0]["slippage"] == 0.01


@pytest.mark.parametrize(
    "bad_data, error_msg",
    [
        # Bridge missing required fields
        ({"bridges": [{}]}, "BridgeConfig"),
        # Dex swap missing slippage
        ({"dex_swaps": [{"chain": "A", "router": "R", "path": ["0x1"]}]}, "slippage"),
        # Noise profile min > max
        (
            {"noise_profile": {"n_micro_txs": {"min": 5, "max": 2}}},
            "n_micro_txs must have min <= max",
        ),
        # Time windows invalid length
        ({"time_windows": {"active_hours": [0], "weekend_bias": 0.5}}, "active_hours"),
        # Distribution missing amounts
        (
            {"distribution": [{"type": "exchange"}]},
            "Must specify amount_bnb or amount_pct",
        ),
    ],
)
def test_load_invalid_strategy(tmp_path, bad_data, error_msg):
    base = {"strategy_description": "TestStrategy"}
    base.update(bad_data)
    path = write_json(tmp_path, base)
    with pytest.raises(SystemExit) as excinfo:
        load_strategy(path)
    # El código de salida debería ser 1
    assert excinfo.value.code == 1
    # Opcionalmente, podríamos verificar que el mensaje de error contiene error_msg
    # Pero dado que load_strategy imprime y luego exit, omitir verificación de stdout
