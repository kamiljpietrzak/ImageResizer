# Aplikacja do zmiany rozmiaru obrazów

Ta aplikacja umożliwia zmianę rozmiaru wszystkich obrazów w podanym folderze na wymiary 300x450 pikseli, zachowując przy tym ich jakość. Obrazy są najpierw skalowane z zachowaniem proporcji, a następnie przycinane do docelowego rozmiaru, co zapewnia, że obrazy nie będą zniekształcone.

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
3. Obraz jest zapisywany z wysoką jakością (95%) i optymalizacją

Ta metoda zapewnia, że obrazy nie są zniekształcone (zwężone lub rozciągnięte), ale zachowują swoje naturalne proporcje, a jednocześnie mają dokładnie wymagany rozmiar.

## Obsługiwane formaty obrazów

Aplikacja obsługuje następujące formaty obrazów:
- JPG/JPEG
- PNG
- BMP
- GIF
- TIFF

## Przykłady

1. Przetwórz obrazy z folderu "moje_obrazy" i zapisz je w folderze "przetworzone":
```
python resize_images.py moje_obrazy przetworzone
```

2. Przetwórz obrazy z bieżącego folderu i zapisz je w folderze "nowy_rozmiar":
```
python resize_images.py . nowy_rozmiar
```
