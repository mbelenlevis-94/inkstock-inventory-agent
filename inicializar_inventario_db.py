# inicializar_inventario_db.py
# Tema: Crear la base SQLite + cargar el catálogo (mismo patrón que Semana 5-6)

# ════════════════════════════════════════
# PARTE 1: Imports
# ════════════════════════════════════════

import sqlite3
import pandas as pd

DB_NAME = "inkstock.db"
CSV_CATALOGO = "catalogo_inkstock.csv"

# ════════════════════════════════════════
# PARTE 2: Crear conexión y tabla productos
# ════════════════════════════════════════
# Mismo patrón que ya usaste en el Recommender API: CREATE TABLE IF NOT EXISTS
# + tipos explícitos. Acá no hace falta reexplicar CREATE TABLE, ya lo dominás.

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    stock INTEGER NOT NULL,
    ventas_semana INTEGER NOT NULL,
    precio_unitario INTEGER NOT NULL
)
""")

# Tabla de logs del agente (mismo patrón que agente_logs del Proyecto 1),
# acá guardamos cada corrida del análisis de inventario
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_analisis TEXT NOT NULL,
    producto_id TEXT NOT NULL,
    escenario TEXT NOT NULL,
    detalle TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos (id)
)
""")

conn.commit()

# ════════════════════════════════════════
# PARTE 3: Cargar el catálogo desde el CSV
# ════════════════════════════════════════
# INSERT OR REPLACE: si corrés el script de nuevo, no duplica productos,
# actualiza los que ya existen (útil mientras estamos armando el proyecto
# y regenerando el catálogo varias veces)

df = pd.read_csv(CSV_CATALOGO)

for _, row in df.iterrows():
    cursor.execute("""
        INSERT OR REPLACE INTO productos (id, nombre, categoria, stock, ventas_semana, precio_unitario)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (row["id"], row["nombre"], row["categoria"], int(row["stock"]),
          int(row["ventas_semana"]), int(row["precio_unitario"])))

conn.commit()

# ════════════════════════════════════════
# DEMOSTRACIÓN / VERIFICACIÓN
# ════════════════════════════════════════

cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]
print(f"✅ Base de datos creada: {DB_NAME}")
print(f"✅ Tablas: productos, inventario_logs")
print(f"✅ Productos cargados: {total}")

print("\nPreview (3 productos random):")
cursor.execute("SELECT id, nombre, categoria, stock, ventas_semana FROM productos ORDER BY RANDOM() LIMIT 3")
for row in cursor.fetchall():
    print(f"  {row}")

conn.close()
