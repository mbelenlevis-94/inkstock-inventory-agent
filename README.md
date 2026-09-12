# 📦 InkStock — Agente de Análisis de Inventario

Agente de monitoreo automático que analiza el catálogo completo de una tienda ficticia de insumos de tatuaje, detecta patrones de rotación de stock y genera reportes accionables sin intervención manual.

Proyecto personal de portfolio, desarrollado de forma autodidacta como parte de mi formación práctica en desarrollo de agentes de IA.

---

## 🎯 Qué hace

El agente recorre todo el inventario de **InkStock** (28 productos, 5 categorías) y clasifica cada producto en uno de 4 escenarios según reglas de negocio configurables:

| Escenario | Condición | Acción sugerida |
|---|---|---|
| 🔴 **CRÍTICO** | Stock bajo + alta demanda | Reponer urgente |
| 🟡 **ALERTA** | Stock bajo | Reponer pronto |
| 🔵 **PROMOCIÓN** | Baja rotación | Candidato a liquidar |
| ⚪ **NORMAL** | Sin condiciones de riesgo | Sin acción |

El reporte se guarda en base de datos y, opcionalmente, Claude API redacta un resumen en lenguaje natural para el dueño de la tienda.

---

## 🏗️ Arquitectura

```
SQLite (productos)
      │
      ▼
Python/Pandas recorre TODO el catálogo
      │
      ▼
Aplica 3 reglas de negocio (if/elif, sin IA)
      │
      ▼
Genera reporte: CRÍTICOS / ALERTAS / PROMOCIONES / NORMALES
      │
      ▼
Guarda en tabla de logs (SQLite)
      │
      ▼
[Opcional] Claude API redacta resumen en lenguaje natural
      │
      ▼
Windows Task Scheduler ejecuta el análisis automáticamente cada día
```

### Decisión de diseño: ¿por qué Python decide y Claude solo redacta?

Este proyecto es el segundo de una serie de dos agentes con arquitecturas deliberadamente distintas:

- **[Proyecto 1 — Agente de Atención al Cliente](https://github.com/mbelenlevis-94/mercadolibre-ai-agent):** agente **conversacional**, responde una pregunta puntual, Claude decide qué Tool llamar según el contexto de la consulta.
- **Este proyecto:** agente de **monitoreo proactivo**, no hay una pregunta — hay que evaluar 28 productos contra reglas numéricas fijas. Delegarle esa decisión a Claude vía Tools implicaría o bien 28 llamadas a la API por corrida (lento, costoso, y reimplementando en lenguaje natural una lógica que ya es determinística), o una sola llamada masiva donde Claude "adivina" umbrales que en realidad son matemática simple.

Por eso acá la decisión de negocio la toma Python directamente, y Claude se reserva para lo que sí aporta valor real: traducir un reporte técnico en un resumen legible para alguien sin conocimientos técnicos.

---

## 📏 Reglas de negocio

```python
STOCK_MINIMO = 8            # por debajo → riesgo de quiebre
UMBRAL_ALTA_ROTACION = 25   # ventas/semana por encima → alta rotación
UMBRAL_BAJA_ROTACION = 3    # ventas/semana por debajo → candidato a promoción
```

---

## 🚀 Cómo correrlo

```bash
# 1. Clonar el repo
git clone https://github.com/mbelenlevis-94/inkstock-inventory-agent.git
cd inkstock-inventory-agent

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
# Crear un archivo .env con:
# ANTHROPIC_API_KEY=tu-api-key-aca

# 4. Generar el catálogo ficticio
python generar_catalogo.py

# 5. Crear la base de datos
python inicializar_inventario_db.py

# 6. Correr el análisis
python agente_inventario.py
```

---

## ⏰ Automatización

El agente puede ejecutarse solo, sin intervención manual, usando Windows Task Scheduler. Instrucciones completas (interfaz gráfica y línea de comandos) en [`programar_tarea.md`](./programar_tarea.md).

```
schtasks /create /tn "InkStock - Analisis Inventario" /tr "ruta\correr_agente.bat" /sc daily /st 09:00
```

---

## 🛠️ Stack técnico

- **Python** — lógica de negocio y orquestación
- **Pandas** — procesamiento del catálogo
- **SQLite** — persistencia de productos y logs de cada corrida
- **Claude API (Anthropic)** — redacción del resumen en lenguaje natural
- **Windows Task Scheduler** — ejecución automática y desatendida

---

## 📁 Estructura del proyecto

```
inkstock-inventory-agent/
├── generar_catalogo.py          # Genera el catálogo ficticio (28 productos)
├── inicializar_inventario_db.py # Crea la base SQLite y carga el catálogo
├── agente_inventario.py         # Agente principal: analiza y reporta
├── correr_agente.bat            # Wrapper para Task Scheduler
├── programar_tarea.md           # Instrucciones de automatización
├── requirements.txt
└── catalogo_inkstock.csv / .json
```

---

## 🔭 Próximos pasos

- [ ] Redacción de resumen con Claude API en producción (endpoint activo)
- [ ] Dashboard simple para visualizar el histórico de `inventario_logs`
- [ ] Agente #3 de la serie: arquitectura con configuración por usuario final

---

## 👤 Autor

**María Belén Levis** — [GitHub](https://github.com/mbelenlevis-94)

Parte de una serie de proyectos de portfolio en desarrollo de agentes de IA aplicados a e-commerce y gestión de inventario.
