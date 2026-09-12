# programar_tarea.md
## Cómo programar el Agente de Inventario para que corra solo

---

## Requisito previo

Tener `correr_agente.bat` en la raíz de `inkstock-inventory-agent`, con la ruta
correcta a tu carpeta (revisá que coincida con dónde está el proyecto en tu PC).

---

## Opción A: Interfaz gráfica (recomendada la primera vez)

1. Buscá "Programador de tareas" en el menú de inicio de Windows (o "Task Scheduler")
2. Click derecho en "Biblioteca del Programador de tareas" → **Crear tarea básica**
3. **Nombre:** `InkStock - Analisis de Inventario`
4. **Descripción:** `Corre el agente de analisis de inventario de InkStock`
5. **Desencadenador (trigger):** elegí frecuencia — para probar, "Diariamente" a una hora cercana a la actual
6. **Acción:** "Iniciar un programa"
7. **Programa o script:** click en "Examinar" y seleccioná `correr_agente.bat`
8. Finalizar

### Verificación

- Click derecho en la tarea creada → **Ejecutar** (para probarla ya, sin esperar al horario)
- Abrí `logs_agente.txt` en la carpeta del proyecto — debería tener el mismo reporte
  que ves cuando corrés `python agente_inventario.py` manualmente
- Si no aparece nada o hay error, revisá la ruta dentro de `correr_agente.bat`

---

## Opción B: Línea de comandos (más rápido si ya conocés el flujo)

Un solo comando, desde una terminal con permisos de administrador:

```
schtasks /create /tn "InkStock - Analisis Inventario" /tr "C:\Users\Belen\OneDrive\Desktop\AGENTES\inkstock-inventory-agent\correr_agente.bat" /sc daily /st 09:00
```

**Desglose del comando:**
- `/tn` → nombre de la tarea
- `/tr` → ruta al .bat que se ejecuta
- `/sc daily` → frecuencia (daily, hourly, weekly también existen)
- `/st 09:00` → hora de inicio

### Verificar que se creó

```
schtasks /query /tn "InkStock - Analisis Inventario"
```

### Eliminarla (si querés probar de nuevo o cambiar la config)

```
schtasks /delete /tn "InkStock - Analisis Inventario" /f
```

---

## Nota sobre OneDrive

Como tu carpeta está dentro de OneDrive (`Desktop\AGENTES\...`), si la PC está
apagada o sin conexión a la hora programada, la tarea simplemente no corre ese día
(no hay "recuperación" automática salvo que actives esa opción en las Configuraciones
avanzadas de la tarea → "Ejecutar tarea tan pronto como sea posible después de una
hora de inicio programada omitida").
