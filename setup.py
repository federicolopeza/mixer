from setuptools import setup, find_packages

setup(
    name="epic_mixer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "web3",
        "rich",
        "aiohttp",
        "qrcode",
        "mnemonic",
        "pycryptodome",
        "ccxt",
        "apscheduler",
        "redis",
        "numpy",
        "scipy",
        "aiohttp-socks",
        "stem",
        "pytest",
        "pytest-asyncio",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "run_mixer=epic_mixer.main:run",
        ],
    },
) 