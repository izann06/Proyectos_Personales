@echo off
chcp 65001 >nul
echo.
echo  ██████╗  █████╗ ██████╗ ██╗  ██╗    ██████╗  █████╗ ███████╗███████╗
echo  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝    ██╔══██╗██╔══██╗██╔════╝██╔════╝
echo  ██║  ██║███████║██████╔╝█████╔╝     ██████╔╝███████║███████╗███████╗
echo  ██║  ██║██╔══██║██╔══██╗██╔═██╗     ██╔═══╝ ██╔══██║╚════██║╚════██║
echo  ██████╔╝██║  ██║██║  ██║██║  ██╗    ██║     ██║  ██║███████║███████║
echo  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
echo.
echo              B A C K U P  -  Instalador
echo  ─────────────────────────────────────────────────────────────
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python no esta instalado o no esta en el PATH.
    echo  Descargalo desde https://www.python.org/downloads/
    echo  Asegurate de marcar "Add Python to PATH" durante la instalacion.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo  [OK] %PYTHON_VER% detectado.

:: Instalar dependencias
echo.
echo  [1/3] Instalando dependencias...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  [ERROR] Fallo al instalar dependencias.
    pause
    exit /b 1
)
echo  [OK] Dependencias instaladas.

:: Buscar pythonw.exe
echo.
echo  [2/4] Buscando pythonw.exe...
for /f "tokens=*" %%i in ('python -c "import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'pythonw.exe'))"') do set PYTHONW=%%i

if not exist "%PYTHONW%" (
    :: Fallback: usar python.exe normal
    for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHONW=%%i
)
echo  [OK] Python encontrado en: %PYTHONW%

:: Obtener directorio actual del proyecto
set PROJECT_DIR=%~dp0
:: Quitar la barra final
if "%PROJECT_DIR:~-1%"=="\" set PROJECT_DIR=%PROJECT_DIR:~0,-1%

set MAIN_SCRIPT=%PROJECT_DIR%\main.py
set WATCHER_SCRIPT=%PROJECT_DIR%\src\startup_watcher.py
set ICON_FILE=%PROJECT_DIR%\app.ico

echo  [OK] Proyecto en: %PROJECT_DIR%

:: Crear acceso directo en el Escritorio usando PowerShell
echo.
echo  [3/4] Creando acceso directo en el Escritorio...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$Desktop = [Environment]::GetFolderPath('Desktop'); " ^
  "$Shortcut = $WshShell.CreateShortcut($Desktop + '\Dark Passenger Backup.lnk'); " ^
  "$Shortcut.TargetPath = '%PYTHONW%'; " ^
  "$Shortcut.Arguments = '\""%MAIN_SCRIPT%\"\"'; " ^
  "$Shortcut.WorkingDirectory = '%PROJECT_DIR%'; " ^
  "$Shortcut.IconLocation = '%ICON_FILE%'; " ^
  "$Shortcut.Description = 'Dark Passenger Backup'; " ^
  "$Shortcut.Save(); " ^
  "Write-Host '[OK] Acceso directo creado en el Escritorio.'"

:: Crear acceso directo en la carpeta Startup (inicio automatico con Windows)
echo.
echo  [4/4] Configurando inicio automatico con Windows...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$WshShell = New-Object -ComObject WScript.Shell; " ^
  "$Startup = $WshShell.SpecialFolders('Startup'); " ^
  "$Shortcut = $WshShell.CreateShortcut($Startup + '\DarkPassenger Watcher.lnk'); " ^
  "$Shortcut.TargetPath = '%PYTHONW%'; " ^
  "$Shortcut.Arguments = '\""%WATCHER_SCRIPT%\"\"'; " ^
  "$Shortcut.WorkingDirectory = '%PROJECT_DIR%'; " ^
  "$Shortcut.IconLocation = '%ICON_FILE%'; " ^
  "$Shortcut.Description = 'Dark Passenger - Vigilante de SSD'; " ^
  "$Shortcut.WindowStyle = 7; " ^
  "$Shortcut.Save(); " ^
  "Write-Host '[OK] Inicio automatico configurado.'"

echo.
echo  ─────────────────────────────────────────────────────────────
echo   Instalacion completada.
echo.
echo   En tu Escritorio: "Dark Passenger Backup" (abre la app)
echo   Inicio automatico: activo (vigila tu SSD en segundo plano)
echo.
echo   Conecta tu SSD en cualquier momento y la app se abrira
echo   automaticamente preguntandote si quieres hacer backup.
echo  ─────────────────────────────────────────────────────────────
echo.
pause

