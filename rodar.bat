@echo off
title Duetti Monitor
color 0A

echo ===========================================
echo        A INICIAR O ROBO DA DUETTI...
echo ===========================================
echo.

:: Executa exatamente o ficheiro que alterámos acima
python monitor_duetti.py

if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo ===========================================
    echo ❌ ERRO CRITICO: O ROBO FECHOU INESPERADAMENTE!
    echo ===========================================
    pause
    exit
)

echo.
echo ===========================================
echo     CONCLUIDO! A ABRIR O DASHBOARD...
echo ===========================================

start "" "index.html"
pause
