# Roadmap de Mejoras para SuperMixer v2

## Fase 1 (0–30 días): Showstoppers y fundamento "Beta mínimo"  
- **R1: Acceso completo al código y dependencias**  
  - Proporcionar/revisar `requirements.txt` y todo el código fuente.  
  - Instalar en modo editable, fijar versiones críticas.  
- **R2: Gestión robusta de dependencias**  
  - Generar/pinnear `requirements.txt` (pip-compile).  
  - Escanear con Safety y resolver vulnerabilidades críticas/altas.  
- **R3: Seguridad criptográfica AES-GCM**  
  - Auditar unicidad de IVs en todos los cifrados.  
  - Añadir tests específicos de IVs y longitudes de etiqueta.  
- **R4: Manejo seguro de claves privadas**  
  - Revisar flujo y almacenamiento de mnemónicos/keys.  
  - Asegurar uso de variables de entorno y evitar hard-code.  
- **R5: Validación de entradas CLI & `strategy.json`**  
  - Implementar esquema (pydantic/voluptuous) para configuración.  
  - Añadir tests de inputs malformados.  

## Fase 2 (31–60 días): Harden de calidad y primeras pruebas E2E  
- **R6: Integración de análisis estático**  
  - Integrar Flake8, Pylint, Mypy y Bandit en CI.  
  - Corregir issues críticos/High de cada herramienta.  
- **R7: Primeros tests End-to-End en testnet**  
  - Script E2E básico: `run_mixer.py --network testnet`.  
  - Validar flujo completo y capturar excepciones.  
- **R8: Fortalecer interacciones con puentes/DEXs**  
  - Añadir manejo de errores, control de slippage configurable.  
  - Mitigaciones básicas contra front-running.  
- **R9: Pruebas exhaustivas de Failover**  
  - Simular fallos de RPC/bridge/DEX y disparar vault recovery.  
  - Validar que los fondos siempre acaben en la bóveda de emergencia.  
- **R10: Revisión y tests de Merkle proofs**  
  - Unit tests para árboles balanceados y no balanceados.  
  - Verificar salado de hojas y root nonce.  

## Fase 3 (61–90 días): Cobertura, robustez y refinamiento  
- **R11: Ampliar cobertura de unit + integración**  
  - Objetivo ≥ 85 % (mock Web3, scheduler edge-cases).  
- **R12: Mejora de logging y reporte de errores**  
  - Estructurar logs (JSON, niveles), sanitizar datos sensibles.  
  - Integrar Sentry o similar para monitorización de errores.  
- **R13: Evaluación y mejora de aleatoriedad**  
  - Revisar uso de `secrets.SystemRandom`.  
  - Benchmark de patrones temporales y de ruido.  
- **R14: Revisión lógica "Storm"**  
  - Auditoría detallada del motor de transacciones en masa.  
  - Optimizar complejidad ciclomática y flujos async.  
- **R15: Refactorización de código**  
  - Reducir complejidad en módulos críticos (Orchestrator, adapters).  
  - Aplicar SRP/SoC y extraer librerías comunes.  
- **R16: Mejoras en documentación**  
  - Completar docstrings y diagrama Mermaid.  
  - Añadir guía de contribución y casos de uso.  

---  
Este roadmap permite avanzar de forma iterativa: primero resolver los "showstoppers", luego establecer calidad y pruebas, y finalmente optimizar arquitectura, cobertura y documentación para alcanzar una Beta segura y mantenible. 