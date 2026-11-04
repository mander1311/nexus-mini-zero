@echo off
setlocal
cd /d "%~dp0"

python -m pip install -r requirements.txt
python -m PyInstaller --noconsole --onefile --name "NEXUS_MINI_ZERO" app.py

if exist "dist\NEXUS_MINI_ZERO.exe" (
    echo Arquivo gerado: dist\NEXUS_MINI_ZERO.exe
) else (
    echo Arquivo nao gerado. Verifique dependencias e erro do PyInstaller.
)
