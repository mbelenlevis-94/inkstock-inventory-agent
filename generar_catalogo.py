# generar_catalogo.py
# Tema: Generación de dataset ficticio - Proyecto 2 InkStock

# ════════════════════════════════════════
# PARTE 1: Imports
# ════════════════════════════════════════

import pandas as pd
import json

# ════════════════════════════════════════
# PARTE 2: Catálogo ficticio (28 productos, 5 categorías)
# ════════════════════════════════════════
# Cada producto tiene stock y ventas_semana pensados a propósito
# para que, al aplicar las 3 reglas de negocio en agente_inventario.py,
# el catálogo dispare los 4 escenarios posibles: CRÍTICO, ALERTA,
# PROMOCIÓN y NORMAL. Así podés probar el agente sin tener que
# adivinar qué números usar.

productos = [
    # ---- TIN - Tintas (6) ----
    {"id": "TIN01", "nombre": "Tinta Negra Premium 30ml",   "categoria": "TIN", "stock": 35, "ventas_semana": 30, "precio_unitario": 4500},
    {"id": "TIN02", "nombre": "Tinta Roja Vibrante 15ml",    "categoria": "TIN", "stock": 6,  "ventas_semana": 28, "precio_unitario": 3200},
    {"id": "TIN03", "nombre": "Tinta Azul Cobalto 15ml",     "categoria": "TIN", "stock": 20, "ventas_semana": 12, "precio_unitario": 3200},
    {"id": "TIN04", "nombre": "Tinta Blanca Opaca 30ml",     "categoria": "TIN", "stock": 5,  "ventas_semana": 10, "precio_unitario": 4200},
    {"id": "TIN05", "nombre": "Set Tintas Pastel x6",        "categoria": "TIN", "stock": 15, "ventas_semana": 2,  "precio_unitario": 15000},
    {"id": "TIN06", "nombre": "Tinta UV Invisible 15ml",     "categoria": "TIN", "stock": 18, "ventas_semana": 6,  "precio_unitario": 5800},

    # ---- AGU - Agujas (6) ----
    {"id": "AGU01", "nombre": "Agujas Round Liner 5RL",      "categoria": "AGU", "stock": 50, "ventas_semana": 40, "precio_unitario": 800},
    {"id": "AGU02", "nombre": "Agujas Round Shader 7RS",     "categoria": "AGU", "stock": 4,  "ventas_semana": 33, "precio_unitario": 850},
    {"id": "AGU03", "nombre": "Agujas Magnum 9M1",           "categoria": "AGU", "stock": 22, "ventas_semana": 18, "precio_unitario": 900},
    {"id": "AGU04", "nombre": "Agujas Flat Shader 5FS",      "categoria": "AGU", "stock": 7,  "ventas_semana": 20, "precio_unitario": 850},
    {"id": "AGU05", "nombre": "Cartuchos Mixtos x20",        "categoria": "AGU", "stock": 60, "ventas_semana": 1,  "precio_unitario": 12000},
    {"id": "AGU06", "nombre": "Agujas Curved Magnum 11CM",   "categoria": "AGU", "stock": 14, "ventas_semana": 9,  "precio_unitario": 950},

    # ---- CUI - Cuidado Post-Tattoo (6) ----
    {"id": "CUI01", "nombre": "Crema Cicatrizante 100g",     "categoria": "CUI", "stock": 40, "ventas_semana": 27, "precio_unitario": 3800},
    {"id": "CUI02", "nombre": "Film Protector Adhesivo",     "categoria": "CUI", "stock": 3,  "ventas_semana": 26, "precio_unitario": 2100},
    {"id": "CUI03", "nombre": "Espuma Limpiadora Suave",     "categoria": "CUI", "stock": 9,  "ventas_semana": 5,  "precio_unitario": 2900},
    {"id": "CUI04", "nombre": "Aceite Reparador Premium",    "categoria": "CUI", "stock": 25, "ventas_semana": 2,  "precio_unitario": 4700},
    {"id": "CUI05", "nombre": "Loción Hidratante Sin Perfume","categoria": "CUI", "stock": 6,  "ventas_semana": 15, "precio_unitario": 3100},
    {"id": "CUI06", "nombre": "Kit Cuidado Completo",        "categoria": "CUI", "stock": 12, "ventas_semana": 8,  "precio_unitario": 8900},

    # ---- ACC - Accesorios / Equipamiento (5) ----
    {"id": "ACC01", "nombre": "Máquina Rotativa Pro",        "categoria": "ACC", "stock": 5,  "ventas_semana": 3,  "precio_unitario": 45000},
    {"id": "ACC02", "nombre": "Fuente de Alimentación Digital","categoria": "ACC","stock": 10, "ventas_semana": 4,  "precio_unitario": 28000},
    {"id": "ACC03", "nombre": "Grip Ergonómico 25mm",        "categoria": "ACC", "stock": 30, "ventas_semana": 22, "precio_unitario": 3500},
    {"id": "ACC04", "nombre": "Camilla Reclinable",          "categoria": "ACC", "stock": 2,  "ventas_semana": 1,  "precio_unitario": 65000},
    {"id": "ACC05", "nombre": "Lámpara LED de Precisión",    "categoria": "ACC", "stock": 18, "ventas_semana": 0,  "precio_unitario": 22000},

    # ---- CON - Consumibles (5) ----
    {"id": "CON01", "nombre": "Guantes Nitrilo x100",        "categoria": "CON", "stock": 80, "ventas_semana": 45, "precio_unitario": 6500},
    {"id": "CON02", "nombre": "Papel Film 45cm",              "categoria": "CON", "stock": 7,  "ventas_semana": 29, "precio_unitario": 1800},
    {"id": "CON03", "nombre": "Vasos Tinta Descartables x50", "categoria": "CON", "stock": 55, "ventas_semana": 20, "precio_unitario": 2200},
    {"id": "CON04", "nombre": "Cubre Camilla Descartable x50","categoria": "CON", "stock": 4,  "ventas_semana": 2,  "precio_unitario": 3400},
    {"id": "CON05", "nombre": "Toallas Desechables x100",     "categoria": "CON", "stock": 33, "ventas_semana": 3,  "precio_unitario": 4100},
]

# ════════════════════════════════════════
# PARTE 3: Guardar el catálogo (CSV + JSON)
# ════════════════════════════════════════
# CSV: para inicializar_inventario_db.py (Pandas lo carga directo a SQLite)
# JSON: como respaldo legible / útil si después lo consumís desde otro script

df = pd.DataFrame(productos)
df.to_csv("catalogo_inkstock.csv", index=False, encoding="utf-8")

with open("catalogo_inkstock.json", "w", encoding="utf-8") as f:
    json.dump(productos, f, ensure_ascii=False, indent=2)

# ════════════════════════════════════════
# DEMOSTRACIÓN / VERIFICACIÓN RÁPIDA
# ════════════════════════════════════════

print(f"✅ Catálogo generado: {len(productos)} productos")
print(f"✅ Categorías: {df['categoria'].nunique()} -> {sorted(df['categoria'].unique().tolist())}")
print(f"✅ Archivos creados: catalogo_inkstock.csv, catalogo_inkstock.json\n")

print("Distribución por categoría:")
print(df["categoria"].value_counts().sort_index())

print("\nPreview (primeros 5 productos):")
print(df.head())
