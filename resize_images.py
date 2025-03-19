import os
import sys
from PIL import Image, ImageEnhance

def resize_images(input_folder, output_folder, target_width=300, target_height=450, quality=95, sharpen_factor=1.2):
    """
    Zmienia rozmiar wszystkich obrazów w podanym folderze na określone wymiary.
    Obrazy są skalowane z zachowaniem proporcji, a następnie przycinane do docelowego rozmiaru.
    
    Args:
        input_folder (str): Ścieżka do folderu z oryginalnymi obrazami
        output_folder (str): Ścieżka do folderu, gdzie zostaną zapisane przetworzone obrazy
        target_width (int): Docelowa szerokość obrazów (domyślnie 300)
        target_height (int): Docelowa wysokość obrazów (domyślnie 450)
        quality (int): Jakość zapisywanych obrazów JPEG (0-100, domyślnie 95)
        sharpen_factor (float): Współczynnik wyostrzania obrazu (domyślnie 1.2)
    """
    # Sprawdź czy folder wyjściowy istnieje, jeśli nie - utwórz go
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Utworzono folder wyjściowy: {output_folder}")
    
    # Obsługiwane formaty obrazów
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    # Liczniki
    total_images = 0
    processed_images = 0
    
    # Przejdź przez wszystkie pliki w folderze wejściowym
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        
        # Sprawdź czy plik jest obrazem
        if os.path.isfile(file_path) and filename.lower().endswith(supported_formats):
            total_images += 1
            try:
                # Otwórz obraz
                with Image.open(file_path) as img:
                    # Zachowaj oryginalny format i tryb koloru
                    original_format = img.format
                    original_mode = img.mode
                    
                    # Konwersja do trybu RGB jeśli to konieczne (dla lepszej jakości)
                    if original_mode != 'RGB' and original_mode != 'RGBA':
                        img = img.convert('RGB')
                    
                    # Oblicz proporcje obrazu
                    width, height = img.size
                    aspect_ratio = width / height
                    target_ratio = target_width / target_height
                    
                    # Skaluj obraz zachowując proporcje - użyj wyższej rozdzielczości dla lepszej jakości
                    scale_factor = 1.5  # Skaluj do większego rozmiaru, a potem zmniejsz
                    
                    if aspect_ratio > target_ratio:
                        # Obraz jest szerszy niż docelowy - skaluj względem wysokości
                        new_height = int(target_height * scale_factor)
                        new_width = int(new_height * aspect_ratio)
                    else:
                        # Obraz jest wyższy niż docelowy - skaluj względem szerokości
                        new_width = int(target_width * scale_factor)
                        new_height = int(new_width / aspect_ratio)
                    
                    # Skaluj obraz z użyciem wysokiej jakości algorytmu
                    # LANCZOS to najlepszy algorytm dla zmniejszania obrazów
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Przytnij obraz do docelowego rozmiaru
                    left = (new_width - target_width * scale_factor) // 2
                    top = (new_height - target_height * scale_factor) // 2
                    right = left + int(target_width * scale_factor)
                    bottom = top + int(target_height * scale_factor)
                    
                    img_cropped = img_resized.crop((left, top, right, bottom))
                    
                    # Zmniejsz do docelowego rozmiaru
                    img_final = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    
                    # Zastosuj wyostrzanie, aby zrekompensować utratę ostrości podczas zmiany rozmiaru
                    enhancer = ImageEnhance.Sharpness(img_final)
                    img_final = enhancer.enhance(sharpen_factor)
                    
                    # Przygotuj ścieżkę do zapisania przetworzonego obrazu
                    output_path = os.path.join(output_folder, filename)
                    
                    # Zapisz przetworzony obraz z zachowaniem oryginalnego formatu
                    if original_format == 'JPEG' or original_format == 'JPG' or filename.lower().endswith(('.jpg', '.jpeg')):
                        # Dla JPEG ustaw wysoką jakość i wyłącz kompresję stratną
                        img_final.save(output_path, format='JPEG', quality=quality, optimize=True, subsampling=0)
                    elif original_format == 'PNG' or filename.lower().endswith('.png'):
                        # Dla PNG użyj najlepszej kompresji bezstratnej
                        img_final.save(output_path, format='PNG', optimize=True, compress_level=9)
                    elif original_format == 'WEBP' or filename.lower().endswith('.webp'):
                        # Dla WebP ustaw jakość i metodę kompresji
                        img_final.save(output_path, format='WEBP', quality=quality, method=6)
                    else:
                        # Dla innych formatów użyj domyślnych ustawień
                        img_final.save(output_path, quality=quality, optimize=True)
                    
                    processed_images += 1
                    print(f"Przetworzono: {filename}")
            except Exception as e:
                print(f"Błąd podczas przetwarzania {filename}: {e}")
    
    print(f"\nZakończono przetwarzanie obrazów.")
    print(f"Przetworzono {processed_images} z {total_images} obrazów.")
    print(f"Wszystkie przetworzone obrazy zostały zapisane w: {output_folder}")

def main():
    """
    Główna funkcja programu. Przetwarza argumenty wiersza poleceń i uruchamia
    funkcję zmiany rozmiaru obrazów.
    """
    # Domyślne wartości
    input_folder = "."  # Domyślnie bieżący folder
    output_folder = "./resized"  # Domyślnie podfolder 'resized' w bieżącym folderze
    target_width = 300
    target_height = 450
    quality = 95
    sharpen_factor = 1.2
    
    # Sprawdź argumenty wiersza poleceń
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    
    # Uruchom funkcję zmiany rozmiaru obrazów
    print(f"Zmiana rozmiaru obrazów z folderu: {input_folder}")
    print(f"Docelowy rozmiar: {target_width}x{target_height} pikseli")
    print(f"Jakość: {quality}, Wyostrzanie: {sharpen_factor}")
    resize_images(input_folder, output_folder, target_width, target_height, quality, sharpen_factor)

if __name__ == "__main__":
    main()
