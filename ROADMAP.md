# Roadmap SuperMixer v2

Este documento lista todas las mejoras pendientes para completar el "SuperMixer v2" con checklists para ir marcando a medida que se implementan.

## 1. Puentes Cross-Chain
- [x] epic_mixer/bridges/__init__.py – factory de adapters
- [x] epic_mixer/bridges/base.py – clase abstracta BaseBridgeAdapter
- [x] epic_mixer/bridges/cbridge_adapter.py – implementar cBridge (envío, tracking, confirmación)
- [x] epic_mixer/bridges/stargate_adapter.py – implementar Stargate (o equivalente)

## 2. Módulo de Swaps en DEX
- [x] epic_mixer/dex/__init__.py – factory de adapters de DEX
- [x] epic_mixer/dex/pancakeswap_adapter.py – swaps vía PancakeSwap v3
- [x] epic_mixer/dex/oneinch_adapter.py – integración con 1inch API

## 3. Generador de Ruido
- [x] epic_mixer/noise_generator.py – micro-transacciones e interacciones "dust" con contratos populares

## 4. Planificador Temporal
- [x] epic_mixer/scheduler.py – calendarizar fases con apscheduler y delays aleatorios

## 5. Seguridad Operacional (OpSec)
- [x] epic_mixer/opsec.py – TorRPCProvider y anonimato RPC (HTTP/SOCKS)

## 6. Manejo de Fallos y Recuperación
- [x] epic_mixer/failover.py – retries automáticos y vault cold-fallback

## 7. Reporte Avanzado / Pruebas de Merkle
- [x] epic_mixer/utils/advanced_reporting.py – Merkle proofs y view-keys para revelación selectiva

## 8. Integración en el Orquestador
- [x] Fase de puentes (`get_bridge_adapter`)
- [x] Swaps DEX
- [x] Generar ruido antes y después de la tormenta
- [x] Programación vía `MixerScheduler`
- [x] Try/catch con `handle_failover`
- [x] Adjuntar Merkle proofs al reporte final

## 9. CLI y Validación de Configuración
- [x] epic_mixer/cli.py – recapitulación de nuevas secciones en CLI
- [x] epic_mixer/utils/config.py – validación básica de schema de la estrategia

## 10. Documentación
- [x] README.md – documentado flujo "SuperMixer v2" y uso de cada módulo
- [x] .gitignore – configurado para reportes, Redis, logs y credenciales
- [x] requirements.txt – actualizadas dependencias para v2
- [x] strategy_v2.json.example – Ejemplo creado

## 11. Dependencias
- [x] `requirements.txt` – dependencias de v2 incluidas

## 12. Pruebas Automáticas
- [x] tests/unit/bridges
- [x] tests/unit/dex
- [x] tests/unit/noise_generator
- [x] tests/unit/scheduler
- [x] tests/integration/failover

*Marca cada ítem como completado cuando implementes el módulo o la tarea correspondiente.* 