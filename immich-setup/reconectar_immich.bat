@echo off
title Reconectar Immich al SSD Externo
color 0B

echo ==========================================================
echo        RECONECTANDO DISCO SSD (E:) A DOCKER E IMMICH
echo ==========================================================
echo.

echo [1/2] Montando disco E: dentro del subsistema de Docker...
wsl -d docker-desktop mount -t drvfs E: /mnt/host/e

echo [2/2] Reiniciando el servidor de Immich...
docker restart immich_server

echo.
echo ==========================================================
echo   EXITO: Immich vuelve a estar conectado y operativo!
echo   Web: http://localhost:2283 o http://192.168.1.129:2283
echo ==========================================================
echo.
pause
