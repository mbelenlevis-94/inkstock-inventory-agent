# agente_inventario.py
# Tema: Agente de monitoreo - Python/Pandas decide, Claude redacta el resumen

# ════════════════════════════════════════
# PARTE 1: Imports y configuración
# ════════════════════════════════════════

import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

DB_NAME = "inkstock.db"

# Reglas de negocio (definidas en la planificación)
STOCK_MINIMO = 8
UMBRAL_ALTA_ROTACION = 25
UMBRAL_BAJA_ROTACION = 3


# ════════════════════════════════════════
# PARTE 2: Lógica de las 3 reglas de negocio
# ════════════════════════════════════════
# Esta es la función que REALMENTE decide - nada de esto pasa por Claude.
# El orden de los if/elif importa (ya lo validamos con el caso CON04):
# el chequeo de stock bajo tiene prioridad sobre el de baja rotación.

def evaluar_producto(producto):
    """
    Recibe un dict con id, nombre, categoria, stock, ventas_semana.
    Devuelve (escenario, detalle) según las 3 reglas de negocio.
    """
    stock = producto["stock"]
    ventas = producto["ventas_semana"]

    if stock < STOCK_MINIMO:
        if ventas > UMBRAL_ALTA_ROTACION:
            return "CRITICO", f"Stock bajo ({stock}) y alta demanda ({ventas}/sem) — reponer urgente"
        else:
            return "ALERTA", f"Stock bajo ({stock}) — reponer pronto"
    elif ventas < UMBRAL_BAJA_ROTACION:
        return "PROMOCION", f"Baja rotación ({ventas}/sem) — candidato a liquidar stock"
    else:
        return "NORMAL", "Sin acción requerida"


# ════════════════════════════════════════
# PARTE 3: Recorrer TODO el catálogo (no espera una pregunta)
# ════════════════════════════════════════

def analizar_inventario():
    """
    Lee todos los productos de la DB, aplica evaluar_producto a cada uno,
    y devuelve una lista de resultados con el escenario ya calculado.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()

    resultados = []
    for producto in productos:
        escenario, detalle = evaluar_producto(producto)
        resultados.append({**producto, "escenario": escenario, "detalle": detalle})

    return resultados


# ════════════════════════════════════════
# PARTE 4: Guardar el reporte en inventario_logs
# ════════════════════════════════════════

def guardar_log(resultados):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for r in resultados:
        cursor.execute("""
            INSERT INTO inventario_logs (fecha_analisis, producto_id, escenario, detalle)
            VALUES (?, ?, ?, ?)
        """, (fecha, r["id"], r["escenario"], r["detalle"]))

    conn.commit()
    conn.close()
    return fecha


# ════════════════════════════════════════
# PARTE 5: Claude redacta el resumen (NO decide, solo comunica)
# ════════════════════════════════════════

def generar_resumen_claude(resultados):
    """
    Le pasamos a Claude el reporte YA CALCULADO por Python.
    Su trabajo es redactarlo en lenguaje natural para un dueño de tienda,
    no volver a evaluar ninguna regla.
    """
    criticos = [r for r in resultados if r["escenario"] == "CRITICO"]
    alertas = [r for r in resultados if r["escenario"] == "ALERTA"]
    promos = [r for r in resultados if r["escenario"] == "PROMOCION"]

    resumen_datos = {
        "criticos": [{"nombre": r["nombre"], "stock": r["stock"], "ventas": r["ventas_semana"]} for r in criticos],
        "alertas": [{"nombre": r["nombre"], "stock": r["stock"], "ventas": r["ventas_semana"]} for r in alertas],
        "promociones": [{"nombre": r["nombre"], "ventas": r["ventas_semana"]} for r in promos],
    }

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Sos el asistente de inventario de InkStock, una tienda de insumos de tatuaje.
Te paso el análisis YA CALCULADO del catálogo (no reevalúes nada, solo redactalo claro):

{resumen_datos}

Escribí un resumen breve en español para el dueño de la tienda:
- Qué productos son urgentes (CRÍTICO)
- Qué productos hay que vigilar (ALERTA)
- Qué productos conviene poner en promoción
- Tono directo, profesional, sin vueltas. Máximo 150 palabras."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


# ════════════════════════════════════════
# DEMOSTRACIÓN / EJECUCIÓN PRINCIPAL
# ════════════════════════════════════════

if __name__ == "__main__":
    resultados = analizar_inventario()

    criticos = [r for r in resultados if r["escenario"] == "CRITICO"]
    alertas = [r for r in resultados if r["escenario"] == "ALERTA"]
    promos = [r for r in resultados if r["escenario"] == "PROMOCION"]
    normales = [r for r in resultados if r["escenario"] == "NORMAL"]

    print(f"📊 ANÁLISIS DE INVENTARIO - InkStock")
    print(f"Total productos analizados: {len(resultados)}\n")

    print(f"🔴 CRÍTICOS ({len(criticos)}):")
    for r in criticos:
        print(f"  - {r['nombre']}: {r['detalle']}")

    print(f"\n🟡 ALERTAS ({len(alertas)}):")
    for r in alertas:
        print(f"  - {r['nombre']}: {r['detalle']}")

    print(f"\n🔵 PROMOCIONES SUGERIDAS ({len(promos)}):")
    for r in promos:
        print(f"  - {r['nombre']}: {r['detalle']}")

    print(f"\n⚪ NORMALES: {len(normales)}")

    fecha = guardar_log(resultados)
    print(f"\n✅ Reporte guardado en inventario_logs ({fecha})")

    # Comentado hasta tener la API key configurada en .env:
    # resumen = generar_resumen_claude(resultados)
    # print(f"\n📝 RESUMEN (Claude):\n{resumen}")
