@echo off
cd /d "%~dp0"

if not exist requirements.txt (
    echo Fehler: requirements.txt wurde in diesem Ordner nicht gefunden.
    pause
    exit /b 1
)

py -m venv .venv
if errorlevel 1 (
    echo Fehler beim Erstellen der virtuellen Umgebung.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo Fehler beim Installieren der Pakete.
    pause
    exit /b 1
)

echo Virtuelle Umgebung .venv wurde erstellt und requirements.txt installiert.
pause
