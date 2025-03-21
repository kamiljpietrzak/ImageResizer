# Aplikacja do zmiany rozmiaru obrazów

Ta aplikacja umożliwia zmianę rozmiaru wszystkich obrazów w podanym folderze na wymiary 300x450 pikseli, zachowując przy tym ich jakość. Obrazy są najpierw skalowane z zachowaniem proporcji, a następnie przycinane do docelowego rozmiaru, co zapewnia, że obrazy nie będą zniekształcone.

## Repozytorium GitHub

Kod źródłowy aplikacji jest dostępny na GitHub:
[https://github.com/kamiljpietrzak/ImageResizer](https://github.com/kamiljpietrzak/ImageResizer)

## Wymagania

- Python 3.6 lub nowszy
- Biblioteka Pillow (PIL)

Możesz zainstalować wymagane zależności za pomocą:

```
pip install -r requirements.txt
```

## Użycie

### Aplikacja desktopowa

Najłatwiejszym sposobem korzystania z aplikacji jest uruchomienie wersji desktopowej:

```
uruchom_aplikacje.bat
```

Aplikacja desktopowa pozwala na:
- Wybór folderu z obrazami za pomocą przeglądarki folderów
- Wybór folderu docelowego
- Dostosowanie docelowych wymiarów obrazów
- Dostosowanie jakości obrazów (0-100) i stopnia wyostrzania
- Śledzenie postępu przetwarzania

### Wersja konsolowa

#### Podstawowe użycie

```
python resize_images.py
```

W tym przypadku aplikacja przetworzy wszystkie obrazy w bieżącym folderze i zapisze je w podfolderze `resized`.

#### Zaawansowane użycie

```
python resize_images.py [folder_wejściowy] [folder_wyjściowy]
```

Gdzie:
- `folder_wejściowy` - ścieżka do folderu z oryginalnymi obrazami (domyślnie bieżący folder)
- `folder_wyjściowy` - ścieżka do folderu, gdzie zostaną zapisane przetworzone obrazy (domyślnie podfolder 'resized' w bieżącym folderze)

## Jak działa przetwarzanie obrazów

1. Każdy obraz jest najpierw skalowany z zachowaniem proporcji, tak aby jego szerokość lub wysokość (w zależności od proporcji) odpowiadała docelowym wymiarom
2. Następnie obraz jest przycinany centralnie do dokładnych wymiarów 300x450 pikseli
3. Zastosowane jest wyostrzanie obrazu, aby zrekompensować utratę ostrości podczas zmiany rozmiaru
4. Obraz jest zapisywany z wysoką jakością (95%) i optymalizacją, z zachowaniem oryginalnego formatu

Ta metoda zapewnia, że obrazy nie są zniekształcone (zwężone lub rozciągnięte), ale zachowują swoje naturalne proporcje, a jednocześnie mają dokładnie wymagany rozmiar.

## Zaawansowane techniki poprawy jakości

Aplikacja wykorzystuje szereg technik, aby zminimalizować utratę jakości podczas przetwarzania:

1. **Nadpróbkowanie (Oversampling)** - Obrazy są najpierw skalowane do rozmiaru 1,5 razy większego niż docelowy, a następnie przycinane i zmniejszane do ostatecznego rozmiaru
2. **Wyostrzanie obrazu** - Kompensuje naturalną utratę ostrości podczas zmiany rozmiaru
3. **Optymalizacja dla różnych formatów**:
   - Dla JPEG: Wyłączenie podpróbkowania chrominancji (subsampling=0), co eliminuje artefakty kompresji
   - Dla PNG: Użycie najlepszej kompresji bezstratnej (compress_level=9)
   - Dla WebP: Optymalizacja jakości i metody kompresji (method=6)
   - Dla AVIF: Najwyższa jakość kompresji (speed=0) dla najlepszych rezultatów
4. **Zachowanie oryginalnego formatu** - Aplikacja wykrywa i zachowuje oryginalny format obrazu

## Obsługiwane formaty obrazów

Aplikacja obsługuje następujące formaty obrazów:
- JPG/JPEG
- PNG
- BMP
- GIF
- TIFF
- WebP
- AVIF (wymaga instalacji dodatkowego pakietu pillow-avif-plugin)

## Przykłady

1. Przetwórz obrazy z folderu "moje_obrazy" i zapisz je w folderze "przetworzone":
```
python resize_images.py moje_obrazy przetworzone
```

2. Przetwórz obrazy z bieżącego folderu i zapisz je w folderze "nowy_rozmiar":
```
python resize_images.py . nowy_rozmiar
```

## Instalacja i uruchomienie

### Instalacja z pliku wykonywalnego (dla użytkowników Windows)

1. Pobierz najnowszą wersję aplikacji z sekcji [Releases](https://github.com/kamiljpietrzak/ImageResizer/releases)
2. Rozpakuj plik ZIP do wybranego folderu
3. Uruchom plik `ImageResizer.exe` lub `Uruchom_ImageResizer.bat`

### Instalacja z kodu źródłowego

1. Sklonuj repozytorium:
   ```
   git clone https://github.com/kamiljpietrzak/ImageResizer.git
   ```

2. Przejdź do katalogu projektu:
   ```
   cd ImageResizer
   ```

3. Zainstaluj wymagane zależności:
   ```
   pip install -r requirements.txt
   ```

4. Uruchom aplikację:
   ```
   python resize_app.py
   ```

## Tworzenie pliku wykonywalnego

Aby utworzyć własny plik wykonywalny (EXE) dla systemu Windows:

1. Zainstaluj PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Utwórz plik wykonywalny:
   ```
   pyinstaller --onefile --windowed --name="ImageResizer" resize_app.py
   ```

3. Plik wykonywalny zostanie utworzony w folderze `dist`

## Licencja

Ten projekt jest licencjonowany na warunkach licencji MIT - zobacz plik [LICENSE](LICENSE) dla szczegółów.

## Autor

Kamil Pietrzak
