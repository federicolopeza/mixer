import pytest

from epic_mixer.utils.advanced_reporting import (
    decrypt_proof,
    encrypt_proof,
    generate_view_key,
)


@pytest.mark.parametrize(
    "proof_list",
    [
        ["0xabc", "0x1234", "0xdeadbeef"],
        [],
        ["0x00"],
    ],
)
def test_encrypt_decrypt_proof_roundtrip(proof_list):
    # Generar clave de vista y cifrar
    view_key = generate_view_key()
    encrypted = encrypt_proof(proof_list, view_key)
    assert isinstance(encrypted, bytes)
    # Descifrar y comparar
    decrypted = decrypt_proof(encrypted, view_key)
    assert decrypted == proof_list


def test_encrypt_proof_nonce_uniqueness():
    proof = ["0xabc"]
    view_key = generate_view_key()
    enc1 = encrypt_proof(proof, view_key)
    enc2 = encrypt_proof(proof, view_key)
    # Los ciphertext deben diferir por el nonce
    assert enc1 != enc2
