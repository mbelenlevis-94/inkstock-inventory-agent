@echo off
chcp 65001 >nul
cd /d "C:\Users\Belen\OneDrive\Desktop\AGENTES\inkstock-inventory-agent"
python agente_inventario.py >> logs_agente.txt 2>&1
