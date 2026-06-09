@echo off
title Duetti Monitor
color 0A

echo ===========================================
echo        A INICIAR O ROBO DA DUETTI...
echo ===========================================
echo.

:: Alterado para abrir o ficheiro antigo que deves ter na pasta
python monitor_duetti.py

if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo ===========================================
    echo ❌ ERRO CRITICO: O ROBO FECHOU INESPERADAMENTE!
    echo Por favor, le a mensagem de erro acima para 
    echo perceber o que falhou no Python.
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