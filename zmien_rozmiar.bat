@echo off
echo Aplikacja do zmiany rozmiaru obrazow na 300x450 pikseli
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
echo Rozpoczynam zmiane rozmiaru obrazow...
echo.

REM Uruchom skrypt Python
python resize_images.py

echo.
echo Nacisnij dowolny klawisz, aby zakonczyc...
pause >nul
