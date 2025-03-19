from PIL import Image, features
import sys

def check_avif_support():
    print("Sprawdzanie obsługi formatu AVIF...")
    
    # Sprawdź czy plugin AVIF jest dostępny
    try:
        import pillow_avif
        print("Plugin pillow-avif-plugin jest zainstalowany.")
    except ImportError:
        print("Plugin pillow-avif-plugin NIE jest zainstalowany.")
        print("Aby zainstalować plugin, użyj: pip install pillow-avif-plugin")
        return False
    
    # Sprawdź zarejestrowane rozszerzenia
    extensions = Image.registered_extensions()
    print("\nZarejestrowane rozszerzenia plików:")
    avif_extensions = [ext for ext, format in extensions.items() if format == 'AVIF']
    
    if avif_extensions:
        print(f"Rozszerzenia AVIF: {', '.join(avif_extensions)}")
    else:
        print("Brak zarejestrowanych rozszerzeń dla formatu AVIF.")
    
    # Sprawdź zarejestrowane formaty
    print("\nZarejestrowane formaty:")
    avif_formats = [format for format in Image.MIME.keys() if 'avif' in format.lower()]
    
    if avif_formats:
        print(f"Formaty AVIF: {', '.join(avif_formats)}")
    else:
        print("Brak zarejestrowanych formatów AVIF.")
    
    # Sprawdź czy możemy otworzyć i zapisać plik AVIF
    print("\nSprawdzanie możliwości tworzenia plików AVIF:")
    try:
        # Utwórz prosty obraz
        img = Image.new('RGB', (100, 100), color='red')
        
        # Spróbuj zapisać jako AVIF
        test_path = 'test_avif.avif'
        img.save(test_path, format='AVIF')
        print(f"Pomyślnie utworzono plik testowy: {test_path}")
        
        # Spróbuj otworzyć plik AVIF
        with Image.open(test_path) as img_loaded:
            print(f"Pomyślnie otworzono plik AVIF. Format: {img_loaded.format}, Rozmiar: {img_loaded.size}")
        
        return True
    except Exception as e:
        print(f"Błąd podczas testowania formatu AVIF: {e}")
        return False

if __name__ == "__main__":
    result = check_avif_support()
    if result:
        print("\nTest zakończony SUKCESEM. Format AVIF jest w pełni obsługiwany.")
    else:
        print("\nTest zakończony NIEPOWODZENIEM. Format AVIF nie jest w pełni obsługiwany.")
    
    sys.exit(0 if result else 1)
