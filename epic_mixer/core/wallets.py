from typing import List
from eth_account import Account as EthAccount
from eth_account.signers.local import LocalAccount
from mnemonic import Mnemonic
from rich.console import Console

log = Console()

def generar_nuevo_mnemonic() -> str:
    """Genera una nueva frase mnemónica segura de 12 palabras."""
    log.print("[cyan]🔑 Generando nuevo mnemónico seguro para la sesión...")
    return Mnemonic("english").generate(strength=128)

def derivar_wallets(mnemonic: str, cantidad: int, start_index: int = 0) -> List[LocalAccount]:
    """Deriva wallets desde un índice inicial, mostrando progreso."""
    EthAccount.enable_unaudited_hdwallet_features()
    wallets = []
    log.print(f"⚙️  Derivando {cantidad} wallets desde el mnemónico de la sesión...")
    for i in range(start_index, start_index + cantidad):
        acct = EthAccount.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/{i}")
        wallets.append(acct)
    log.print("[green]✅ Wallets derivadas correctamente.")
    return wallets 