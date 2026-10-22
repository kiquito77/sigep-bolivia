@echo off
title Sistema SIGEP Presupuestario y Contable
color 0b
echo =====================================================================
echo                SISTEMA SIGEP BOLIVIA (SIGEPMV)
echo       Presupuestos del Sector Publico y Contabilidad Integrada
echo =====================================================================
echo.
echo Iniciando servidor y abriendo aplicacion...
cd /d "%~dp0"

start "" http://localhost:8000
python server.py

pause
