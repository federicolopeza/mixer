# Epic Mixer 🌪️
### An Experimental Multi-Layer Transaction Obfuscation Orchestrator for BSC

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
![Status: Experimental](https://img.shields.io/badge/status-experimental-red.svg)

**Epic Mixer** is a command-line framework designed for advanced, experimental research into blockchain transaction privacy. It functions as a sophisticated **orchestrator**, executing user-defined strategies to fragment and obfuscate transaction trails on the Binance Smart Chain (BSC) across multiple layers and systems.

---

## ⚠️ EXTREMELY IMPORTANT: This is an Experimental Tool

**USE AT YOUR OWN IMMENSE RISK. THIS IS NOT A TOOL FOR ILLEGAL ACTIVITIES. IT IS A RESEARCH FRAMEWORK.**

-   **High Risk of Fund Loss**: This software is complex and experimental. Misconfiguration, network errors, or undiscovered bugs can and likely will lead to the **total and irreversible loss of funds**.
-   **No Guarantees of Privacy**: While it aims to dramatically complicate transaction analysis, it **cannot guarantee absolute anonymity**. Determined adversaries with sufficient resources may still be able to trace funds.
-   **For Educational & Research Purposes Only**: This tool was developed to explore concepts of multi-system transaction obfuscation. The developers are not responsible for any use, misuse, or loss of assets.

---

## 🏛️ Core Concepts & Architecture

Epic Mixer is not a simple "tumbler." It's an **orchestrator** that you command. The core philosophy is **multi-layered, strategy-driven obfuscation**.

1.  **Strategy-Driven**: You define the entire mixing plan in a `strategy.json` file. This includes the number of wallets, mixing rounds, and, most importantly, the **distribution legs**.
2.  **Multi-Layer Distribution**: Instead of a single destination, the funds are fragmented and sent through multiple "legs," such as:
    -   **Exchanges**: A portion of funds can be sent to a deposit address you provide from an external exchange.
    -   **Privacy Pools (Simulated)**: A portion can be sent to an intermediary wallet to simulate interaction with a privacy protocol like Tornado Cash.
    -   **Direct Fragmentation**: The remainder can be distributed directly to your final destination wallets.
3.  **Non-Custodial & Ephemeral**: The tool operates on a "Safe Box" model. It generates a new, ephemeral mnemonic and deposit address for each session. **You never enter your private keys.** You send funds *to* the script's temporary wallet.
4.  **Encrypted Reporting**: Upon completion, all session data, including the ephemeral mnemonic and generated private keys, is saved to a password-encrypted file. Without the password, the data is useless.

```mermaid
graph TD
    subgraph " "
        direction LR
        U[👨‍💻 Tú]
    end

    subgraph "Proyecto Epic Mixer (Tu Máquina Local)"
        RUN[▶️ run_mixer.py]

        subgraph "Paquete epic_mixer"
            MAIN[🎬 main.py<br/>(El Director)]
            subgraph "Módulos de Utilidades"
                CONF[📄 utils/config.py]
                REP[📦 utils/reporting.py]
            end
            subgraph "Módulos del Núcleo"
                W3U[🔗 core/web3_utils.py]
                WLT[🔑 core/wallets.py]
                ORCH[🌪️ core/orchestrator.py]
            end
            subgraph "Interfaz de Usuario"
                CLI[🗣️ cli.py]
            end
        end
    end
    
    subgraph " "
        direction LR
        BLOCKCHAIN[🌐 Binance Smart Chain]
    end
    
    subgraph " "
        direction LR
        OUT[📄 reporte_encriptado.dat]
    end


    U -- "Ejecuta" --> RUN
    RUN -- "Inicia" --> MAIN
    
    MAIN -- "1. Carga estrategia" --> CONF
    MAIN -- "2. Crea sesión" --> WLT
    
    MAIN -- "3. Espera depósito" --> W3U
    W3U -- "Muestra QR" --> U
    U -- "Envía BNB" --> BLOCKCHAIN
    BLOCKCHAIN -- "Detecta fondos" --> W3U
    
    W3U -- "Notifica a" --> MAIN
    MAIN -- "4. Pide datos" --> CLI
    CLI -- "Pregunta destinos y pass" --> U
    U -- "Introduce datos" --> CLI
    CLI -- "Devuelve a" --> MAIN
    
    MAIN -- "5. ¡EJECUTAR!" --> ORCH
    ORCH -- "Envía TXs" --> BLOCKCHAIN
    
    ORCH -- "Finalizado" --> MAIN
    MAIN -- "6. Crea reporte" --> REP
    REP -- "Guarda archivo" --> OUT
```

---

## 📋 Requirements

-   Python 3.9+

## 🚀 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd epic-mixer
    ```

2.  **Set up a Virtual Environment (Highly Recommended)**:
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create Your Strategy**:
    -   Copy the example strategy file:
        ```bash
        cp strategy.json.example strategy.json
        ```
    -   **Edit `strategy.json`** to define your desired obfuscation plan.

---

## ▶️ How to Use

The entire process is orchestrated through the command line.

### Step 1: Launch the Mixer

Execute the script from the root directory. Use the `--network` flag for mainnet operations.

```bash
# To run on the SAFE, FREE Testnet (DEFAULT)
python run_mixer.py

# To run on the REAL, RISKY Mainnet
python run_mixer.py --network mainnet
```

### Step 2: Deposit Funds

The script will generate and display a unique, one-time deposit address and a QR code. Send the BNB you wish to process to this address from your secure wallet or exchange. The script will wait and automatically detect the deposit.

### Step 3: Configure Destinations

Once funds are detected, the script will guide you through a series of prompts based on your `strategy.json` file:

-   It will ask you to provide deposit addresses for any `exchange` legs.
-   It will ask you how many final wallets you want and their addresses.
-   Finally, it will ask for a **strong password** to encrypt the final report file.

### Step 4: Execution & Reporting

After your final confirmation, the orchestrator will execute the strategy. Upon completion, it will generate an encrypted file named `mixer_report_encrypted_...dat`.

---

##  decryption-tool.py

To decrypt and view your session report, you will need a separate script.
You can create a new file and add this to it.
```python
import getpass
import json
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

SALT_SIZE = 16
NONCE_SIZE = 16
TAG_SIZE = 16
KEY_SIZE = 32

def decrypt_data(encrypted_data: bytes, password: str) -> dict:
    """Desencripta datos encriptados con AES-256-GCM."""
    try:
        salt = encrypted_data[:SALT_SIZE]
        nonce = encrypted_data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        tag = encrypted_data[SALT_SIZE + NONCE_SIZE:SALT_SIZE + NONCE_SIZE + TAG_SIZE]
        ciphertext = encrypted_data[SALT_SIZE + NONCE_SIZE + TAG_SIZE:]

        key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=1000000)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

        decrypted_payload = cipher.decrypt_and_verify(ciphertext, tag)
        
        return json.loads(decrypted_payload.decode('utf-8'))
    except (ValueError, KeyError):
        raise ValueError("Error de desencriptación. Contraseña incorrecta o datos corruptos.")

def main():
    """CLI para desencriptar un reporte."""
    print("--- Epic Mixer Report Decryptor ---")
    file_path = input("Arrastra o pega la ruta al archivo .dat encriptado: ").strip().replace("'", "")
    
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print("❌ Error: Archivo no encontrado.")
        return
        
    password = getpass.getpass("🔑 Introduce la contraseña de la sesión: ")
    
    try:
        decrypted_report = decrypt_data(encrypted_data, password)
        print("\n--- ✅ Reporte Desencriptado ---")
        print(json.dumps(decrypted_report, indent=4))
        print("\n------------------------------")
    except ValueError as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 