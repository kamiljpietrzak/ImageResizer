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
echo Podaj sciezke do folderu z obrazami (lub nacisnij Enter, aby uzyc biezacego folderu):
set /p input_folder="> "

if "%input_folder%"=="" set input_folder=.

echo.
echo Podaj sciezke do folderu, gdzie maja zostac zapisane przetworzone obrazy (lub nacisnij Enter, aby uzyc domyslnego folderu 'resized'):
set /p output_folder="> "

if "%output_folder%"=="" set output_folder=resized

echo.
echo Rozpoczynam zmiane rozmiaru obrazow z folderu %input_folder% do folderu %output_folder%...
echo.

REM Uruchom skrypt Python z podanymi parametrami
python resize_images.py "%input_folder%" "%output_folder%"

echo.
echo Nacisnij dowolny klawisz, aby zakonczyc...
pause >nul
