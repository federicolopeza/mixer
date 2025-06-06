import pytest

from epic_mixer.utils.encryption import (
    NONCE_SIZE,
    SALT_SIZE,
    decrypt_data,
    encrypt_data,
)


def test_encrypt_decrypt_data_roundtrip():
    data = {"x": 1, "y": "foo", "z": [1, 2, 3]}
    password = "supersecret"
    encrypted = encrypt_data(data, password)
    # El tamaño debe ser mayor que SALT_SIZE + NONCE_SIZE
    assert isinstance(encrypted, bytes)
    assert len(encrypted) > SALT_SIZE + NONCE_SIZE
    decrypted = decrypt_data(encrypted, password)
    assert decrypted == data


@pytest.mark.parametrize("wrong_pwd", ["bad", "", "1234"])
def test_decrypt_with_wrong_password_raises(wrong_pwd):
    data = {"key": "value"}
    password = "correctpwd"
    encrypted = encrypt_data(data, password)
    with pytest.raises(ValueError):
        decrypt_data(encrypted, wrong_pwd)
