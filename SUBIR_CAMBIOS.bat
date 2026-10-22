@echo off
chcp 65001 > nul
echo ========================================================
echo       SUBIENDO MEJORAS A GITHUB Y RENDER (NUBE)
echo ========================================================
echo.

git add .
set /p mensaje="Escribe el detalle de tu mejora (o presiona ENTER para continuar): "
if "%mensaje%"=="" set mensaje=Mejoras y actualizaciones del sistema SIGEP

git commit -m "%mensaje%"
echo.
echo Enviando cambios a GitHub...
git push origin master

echo.
echo ========================================================
echo  ¡LISTO! Tus cambios se subieron a GitHub.
echo  Render actualizara la nube automaticamente en 1 minuto.
echo ========================================================
echo.
pause
