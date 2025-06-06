# Epic Mixer 🌪️
### Un Orquestador Experimental de Ofuscación de Transacciones Multi-Capa para BSC

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/Licencia-MIT-green.svg)](https://opensource.org/licenses/MIT)
![Estado: Experimental](https://img.shields.io/badge/estado-experimental-red.svg)

**Epic Mixer** es un framework de línea de comandos diseñado para la investigación avanzada y experimental de la privacidad en transacciones de blockchain. Funciona como un **orquestador** sofisticado, ejecutando estrategias definidas por el usuario para fragmentar y ofuscar los rastros de las transacciones en la Binance Smart Chain (BSC) a través de múltiples capas y sistemas.

---

## ⚠️ EXTREMADAMENTE IMPORTANTE: Esta es una Herramienta Experimental

**ÚSALA BAJO TU PROPIO E INMENSO RIESGO. ESTA NO ES UNA HERRAMIENTA PARA ACTIVIDADES ILEGALES. ES UN FRAMEWORK DE INVESTIGACIÓN.**

-   **Alto Riesgo de Pérdida de Fondos**: Este software es complejo y experimental. Una mala configuración, errores de red o bugs no descubiertos pueden y probablemente conducirán a la **pérdida total e irreversible de tus fondos**.
-   **Sin Garantías de Privacidad**: Aunque su objetivo es complicar drásticamente el análisis de transacciones, **no puede garantizar un anonimato absoluto**. Adversarios con suficientes recursos podrían rastrear los fondos.
-   **Solo para Fines Educativos y de Investigación**: Esta herramienta fue desarrollada para explorar conceptos de ofuscación de transacciones multi-sistema. Los desarrolladores no se hacen responsables de ningún uso, mal uso o pérdida de activos.

---

## 🏛️ Conceptos Clave y Arquitectura

Epic Mixer no es un simple "tumbler". Es un **orquestador** que tú diriges. La filosofía central es la **ofuscación multi-capa dirigida por estrategias**.

1.  **Dirigido por Estrategia**: Defines el plan de mezcla completo en un archivo `strategy.json`. Esto incluye el número de wallets, las rondas de mezcla y, lo más importante, los **brazos de distribución** (distribution legs).
2.  **Distribución Multi-Capa**: En lugar de un único destino, los fondos se fragmentan y se envían a través de múltiples "brazos", tales como:
    -   **Exchanges**: Una porción de los fondos puede ser enviada a una dirección de depósito que tú proporciones de un exchange externo.
    -   **Pools de Privacidad (Simulado)**: Una porción puede ser enviada a una wallet intermediaria para simular la interacción con un protocolo de privacidad como Tornado Cash.
    -   **Fragmentación Directa**: El resto puede ser distribuido directamente a tus wallets de destino finales.
3.  **No Custodial y Efímero**: La herramienta opera bajo un modelo de "Caja Fuerte". Genera un nuevo mnemónico efímero y una dirección de depósito para cada sesión. **Nunca introduces tus claves privadas.** Envías los fondos *a* la wallet temporal del script.
4.  **Reportes Encriptados**: Al finalizar, todos los datos de la sesión, incluyendo el mnemónico efímero y las claves privadas generadas, se guardan en un archivo encriptado con contraseña. Sin la contraseña, los datos son inútiles.

```mermaid
graph LR
    subgraph "🔧 Fase 1: Preparación del Sistema"
        direction TB
        U[👨‍💻 Usuario] -.->|"ejecuta comando"| RUN(▶️ run_mixer.py)
        RUN -->|"inicia orquestador"| MAIN{🎬 main.py<br/>Director Central}
        MAIN -->|"lee configuración"| CONF([📄 strategy.json<br/>Plan de Mezcla])
        MAIN -->|"genera sesión efímera"| WLT([🔑 Generador de Wallets<br/>⚡ Temporales])
        WLT -.->|"mnemónico + direcciones"| TEMP[(🗃️ Sesión Temporal)]
    end

    subgraph "💰 Fase 2: Recepción Segura de Fondos"
        direction TB
        TEMP -.->|"dirección de depósito"| W3U([🔗 Monitor Blockchain<br/>Detecta Transacciones])
        W3U -->|"muestra QR + dirección"| DISPLAY[📱 Código QR<br/>+ Dirección BSC]
        DISPLAY -.->|"usuario escanea/copia"| U
        U -->|"envía BNB desde wallet externa"| BLOCKCHAIN[(🌐 Binance Smart Chain<br/>Red Pública)]
        BLOCKCHAIN -->|"transacción detectada ✅"| W3U
        W3U -.->|"fondos confirmados"| BALANCE[💎 Fondos Seguros<br/>En Wallet Temporal]
    end
    
    subgraph "⚙️ Fase 3: Configuración Interactiva"
        direction TB
        BALANCE -.->|"fondos listos"| MAIN
        MAIN -->|"solicita configuración"| CLI([🗣️ Interfaz Interactiva<br/>Recopila Destinos])
        CLI -->|"pregunta direcciones exchange"| PROMPT1[❓ Direcciones de Exchange<br/>para Distribución]
        CLI -->|"pregunta wallets finales"| PROMPT2[❓ Wallets de Destino Final<br/>del Usuario]
        CLI -->|"solicita contraseña segura"| PROMPT3[🔐 Contraseña de Encriptación<br/>para Reporte]
        PROMPT1 & PROMPT2 & PROMPT3 -.->|"datos sensibles"| U
        U -.->|"introduce información"| CLI
        CLI -.->|"configuración completa"| CONFIG[⚡ Plan de Ejecución<br/>Listo para Orquestación]
    end

    subgraph "🌪️ Fase 4: Ejecución y Reporte Final"
        direction TB
        CONFIG -.->|"inicia ejecución"| MAIN
        MAIN -->|"delega orquestación"| ORCH([🎭 Orquestador Épico<br/>Motor de Mezcla])
        ORCH -->|"fragmenta y distribuye"| MULTI[🔀 Distribución Multi-Brazo<br/>Exchanges + Pools + Directa]
        MULTI -->|"ejecuta transacciones"| BLOCKCHAIN
        BLOCKCHAIN -.->|"confirmaciones de red"| ORCH
        ORCH -.->|"ejecución completada ✅"| MAIN
        MAIN -->|"genera reporte detallado"| REP([📊 Generador de Reportes<br/>Recopila Todos los Datos])
        REP -->|"encripta con contraseña"| OUT([📄 Archivo Encriptado<br/>reporte_encriptado.dat])
        OUT -.->|"reporte seguro guardado"| U
    end
    
    %% Estilos para diferencia visual clara
    style U fill:#3B4252,stroke:#81A1C1,color:#ECEFF4,stroke-width:3px
    style BLOCKCHAIN fill:#A3BE8C,stroke:#4C566A,color:#2E3440,stroke-width:3px
    style RUN fill:#BF616A,stroke:#D8DEE9,color:#ECEFF4
    style OUT fill:#EBCB8B,stroke:#4C566A,color:#2E3440
    style TEMP fill:#B48EAD,stroke:#4C566A,color:#ECEFF4
    style BALANCE fill:#88C0D0,stroke:#4C566A,color:#2E3440
    style CONFIG fill:#D08770,stroke:#4C566A,color:#ECEFF4
    style MULTI fill:#A3BE8C,stroke:#4C566A,color:#2E3440
    
    %% Estilos de las fases
    style U fill:#3B4252,stroke:#81A1C1,color:#ECEFF4
    style BLOCKCHAIN fill:#A3BE8C,stroke:#4C566A,color:#2E3440
    style RUN fill:#BF616A,stroke:#D8DEE9,color:#ECEFF4
    style OUT fill:#EBCB8B,stroke:#4C566A,color:#2E3440
```

---

## 📋 Requisitos

-   Python 3.9+

## 🚀 Instalación y Configuración

1.  **Clona el Repositorio**:
    ```bash
    git clone <URL_DE_TU_REPOSITORIO>
    cd epic-mixer
    ```

2.  **Crea un Entorno Virtual (Altamente Recomendado)**:
    ```bash
    python -m venv venv
    # En macOS/Linux:
    source venv/bin/activate
    # En Windows:
    venv\Scripts\activate
    ```

3.  **Instala las Dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crea Tu Estrategia**:
    -   Copia el archivo de estrategia de ejemplo:
        ```bash
        cp strategy.json.example strategy.json
        ```
    -   **Edita `strategy.json`** para definir tu plan de ofuscación.

---

## ▶️ Modo de Uso

Todo el proceso se orquesta a través de la línea de comandos.

### Paso 1: Inicia el Mixer

Ejecuta el script desde el directorio raíz. Usa el flag `--network` para operaciones en la red principal (Mainnet).

```bash
# Para ejecutar en la Testnet SEGURA y GRATUITA (POR DEFECTO)
python run_mixer.py

# Para ejecutar en la Mainnet REAL y RIESGOSA
python run_mixer.py --network mainnet
```

### Paso 2: Deposita los Fondos

El script generará y mostrará una dirección de depósito única y de un solo uso, junto con un código QR. Envía los BNB que deseas procesar a esta dirección desde tu wallet segura o exchange. El script esperará y detectará el depósito automáticamente.

### Paso 3: Configura los Destinos

Una vez detectados los fondos, el script te guiará a través de una serie de preguntas basadas en tu archivo `strategy.json`:

-   Te pedirá que proporciones las direcciones de depósito para cualquier "brazo" de tipo `exchange`.
-   Te preguntará cuántas wallets finales deseas y sus direcciones.
-   Finalmente, te pedirá una **contraseña segura** para encriptar el archivo de reporte final.

### Paso 4: Ejecución y Reporte

Tras tu confirmación final, el orquestador ejecutará la estrategia. Al completarse, generará un archivo encriptado llamado `mixer_report_encrypted_...dat`.

---

##  Herramienta de Desencriptación (decryption-tool.py)

Para desencriptar y ver el reporte de tu sesión, necesitarás un script separado. Puedes crear un nuevo archivo `decryption-tool.py` y añadirle este código:
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
    print("--- Desencriptador de Reportes Epic Mixer ---")
    file_path_input = input("Arrastra o pega la ruta al archivo .dat encriptado: ").strip()
    # Limpiar comillas si el usuario arrastra el archivo (común en Windows)
    file_path = file_path_input.replace("'", "").replace('"', '')
    
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado en la ruta: {file_path}")
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

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
