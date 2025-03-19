@echo off
echo Uruchamianie aplikacji do zmiany rozmiaru obrazow...
echo ======================================================
echo.

REM Sprawdz czy Python jest zainstalowany
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo BLAD: Python nie jest zainstalowany lub nie jest dostepny w PATH.
    echo Prosze zainstalowac Python ze strony https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Instalacja wymaganych bibliotek, jesli nie sa zainstalowane
echo Instalacja wymaganych bibliotek...
pip install -r requirements.txt

echo.
echo Uruchamianie aplikacji...
echo.

REM Uruchom aplikacje
python resize_app.py

exit /b
