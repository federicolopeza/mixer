import hashlib
from typing import List, Dict
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


def _hash_pair(a: bytes, b: bytes) -> bytes:
    return hashlib.sha256(a + b).digest()


def generate_merkle_root(leaves: List[str]) -> str:
    """Genera la raíz Merkle (hex) a partir de una lista de hashes (hex prefijo 0x)."""
    # Convertir a bytes
    nodes = []
    for leaf in leaves:
        h = leaf[2:] if leaf.startswith('0x') else leaf
        nodes.append(bytes.fromhex(h))

    if not nodes:
        return ''

    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        new_level = []
        for i in range(0, len(nodes), 2):
            new_level.append(_hash_pair(nodes[i], nodes[i+1]))
        nodes = new_level

    return '0x' + nodes[0].hex()


def generate_merkle_proof(leaves: List[str], index: int) -> List[str]:
    """Genera la proof (lista de sibling hashes hex) para la hoja en `index`."""
    # Convertir a bytes
    nodes = [bytes.fromhex((leaf[2:] if leaf.startswith('0x') else leaf)) for leaf in leaves]
    proof = []

    idx = index
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        new_level = []
        for i in range(0, len(nodes), 2):
            left, right = nodes[i], nodes[i+1]
            new_level.append(_hash_pair(left, right))
            # Si idx está en este par, registrar el sibling
            if i == idx or i+1 == idx:
                sibling = right if i == idx else left
                proof.append('0x' + sibling.hex())
        idx //= 2
        nodes = new_level
    return proof


def generate_view_key() -> bytes:
    """Genera una clave aleatoria para cifrar/revelar proofs selectivamente."""
    return get_random_bytes(32)


def encrypt_proof(proof: List[str], view_key: bytes) -> bytes:
    """Encripta el proof JSON con AES-GCM."""
    import json
    from Crypto.Cipher import AES

    plaintext = json.dumps(proof).encode('utf-8')
    cipher = AES.new(view_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext


def decrypt_proof(encrypted: bytes, view_key: bytes) -> List[str]:
    """Desencripta el proof usando AES-GCM."""
    import json
    nonce = encrypted[:16]
    tag = encrypted[16:32]
    ciphertext = encrypted[32:]
    cipher = AES.new(view_key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return json.loads(plaintext.decode('utf-8')) 