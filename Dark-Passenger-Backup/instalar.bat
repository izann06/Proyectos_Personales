@echo off
echo.
echo  =============================================================
echo                 DARK PASSENGER BACKUP - INSTALADOR
echo  =============================================================
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
echo  [1/4] Instalando dependencias...
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
    for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHONW=%%i
)
echo  [OK] Python encontrado en: %PYTHONW%

:: Obtener directorio actual del proyecto
set PROJECT_DIR=%~dp0
if "%PROJECT_DIR:~-1%"=="\" set PROJECT_DIR=%PROJECT_DIR:~0,-1%

set MAIN_SCRIPT=%PROJECT_DIR%\main.py
set WATCHER_SCRIPT=%PROJECT_DIR%\src\startup_watcher.py
set ICON_FILE=%PROJECT_DIR%\assets\images\blood_drop.ico

echo  [OK] Proyecto en: %PROJECT_DIR%

:: Crear acceso directo en el Escritorio
echo.
echo  [3/4] Creando acceso directo en el Escritorio...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Dark Passenger Backup.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%PYTHONW%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Arguments = chr(34) ^& "%MAIN_SCRIPT%" ^& chr(34) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%PROJECT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%ICON_FILE%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Dark Passenger Backup" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"
cscript /nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"
echo  [OK] Acceso directo creado en el Escritorio.

:: Crear acceso directo en la carpeta Startup (inicio automatico con Windows)
echo.
echo  [4/4] Configurando inicio automatico con Windows...
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateWatcher.vbs"
echo sLinkFile = oWS.SpecialFolders("Startup") ^& "\DarkPassenger Watcher.lnk" >> "%TEMP%\CreateWatcher.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateWatcher.vbs"
echo oLink.TargetPath = "%PYTHONW%" >> "%TEMP%\CreateWatcher.vbs"
echo oLink.Arguments = chr(34) ^& "%WATCHER_SCRIPT%" ^& chr(34) >> "%TEMP%\CreateWatcher.vbs"
echo oLink.WorkingDirectory = "%PROJECT_DIR%" >> "%TEMP%\CreateWatcher.vbs"
echo oLink.IconLocation = "%ICON_FILE%" >> "%TEMP%\CreateWatcher.vbs"
echo oLink.Description = "Dark Passenger - Vigilante de SSD" >> "%TEMP%\CreateWatcher.vbs"
echo oLink.WindowStyle = 7 >> "%TEMP%\CreateWatcher.vbs"
echo oLink.Save >> "%TEMP%\CreateWatcher.vbs"
cscript /nologo "%TEMP%\CreateWatcher.vbs"
del "%TEMP%\CreateWatcher.vbs"

echo  [OK] Inicio automatico configurado.

echo.
echo  =============================================================
echo   Instalacion completada.
echo.
echo   En tu Escritorio: "Dark Passenger Backup" (abre la app)
echo   Inicio automatico: activo (vigila tu SSD en segundo plano)
echo.
echo   Conecta tu SSD en cualquier momento y la app se abrira
echo   automaticamente preguntandote si quieres hacer backup.
echo  =============================================================
echo.
pause
