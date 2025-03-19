import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageEnhance
import threading
import time

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zmiana rozmiaru obrazów")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        
        # Ustawienie ikony aplikacji (opcjonalnie)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Zmienne
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.target_width = tk.IntVar(value=300)
        self.target_height = tk.IntVar(value=450)
        self.quality = tk.IntVar(value=95)
        self.sharpen_factor = tk.DoubleVar(value=1.2)
        self.progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Gotowy do pracy")
        self.processing = False
        
        # Tworzenie interfejsu
        self.create_widgets()
        
        # Centrowanie okna
        self.center_window()
    
    def create_widgets(self):
        # Główny kontener
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Styl
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6)
        style.configure("TFrame", padding=6)
        
        # Sekcja wyboru folderów
        folder_frame = ttk.LabelFrame(main_frame, text="Wybór folderów", padding="10")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Folder wejściowy
        ttk.Label(folder_frame, text="Folder z obrazami:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folder_frame, textvariable=self.input_folder, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(folder_frame, text="Przeglądaj...", command=self.browse_input_folder).grid(row=0, column=2, padx=5, pady=5)
        
        # Folder wyjściowy
        ttk.Label(folder_frame, text="Folder docelowy:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(folder_frame, textvariable=self.output_folder, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(folder_frame, text="Przeglądaj...", command=self.browse_output_folder).grid(row=1, column=2, padx=5, pady=5)
        
        # Sekcja ustawień rozmiaru
        size_frame = ttk.LabelFrame(main_frame, text="Ustawienia rozmiaru", padding="10")
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Szerokość
        ttk.Label(size_frame, text="Szerokość (px):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(size_frame, textvariable=self.target_width, width=10).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Wysokość
        ttk.Label(size_frame, text="Wysokość (px):").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        ttk.Entry(size_frame, textvariable=self.target_height, width=10).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Sekcja ustawień jakości
        quality_frame = ttk.LabelFrame(main_frame, text="Ustawienia jakości", padding="10")
        quality_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Jakość JPEG
        ttk.Label(quality_frame, text="Jakość (0-100):").grid(row=0, column=0, sticky=tk.W, pady=5)
        quality_scale = ttk.Scale(quality_frame, from_=70, to=100, variable=self.quality, orient=tk.HORIZONTAL, length=150)
        quality_scale.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        # Wyostrzanie
        ttk.Label(quality_frame, text="Wyostrzanie:").grid(row=1, column=0, sticky=tk.W, pady=5)
        sharpen_scale = ttk.Scale(quality_frame, from_=0.8, to=2.0, variable=self.sharpen_factor, orient=tk.HORIZONTAL, length=150)
        sharpen_scale.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(quality_frame, textvariable=self.sharpen_factor).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Sekcja przetwarzania
        process_frame = ttk.Frame(main_frame, padding="10")
        process_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Przycisk przetwarzania
        self.process_button = ttk.Button(process_frame, text="Rozpocznij przetwarzanie", command=self.start_processing)
        self.process_button.pack(pady=10)
        
        # Pasek postępu
        progress_frame = ttk.Frame(main_frame, padding="10")
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        
        ttk.Label(status_frame, textvariable=self.status_text).pack(side=tk.LEFT)
        
        # Informacje
        info_frame = ttk.LabelFrame(main_frame, text="Informacje", padding="10")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        info_text = tk.Text(info_frame, height=6, width=50, wrap=tk.WORD)
        info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        info_text.insert(tk.END, "Aplikacja do zmiany rozmiaru obrazów\n\n")
        info_text.insert(tk.END, "1. Wybierz folder z obrazami\n")
        info_text.insert(tk.END, "2. Wybierz folder docelowy\n")
        info_text.insert(tk.END, "3. Opcjonalnie dostosuj ustawienia rozmiaru i jakości\n")
        info_text.insert(tk.END, "4. Kliknij 'Rozpocznij przetwarzanie'\n\n")
        info_text.insert(tk.END, "Obrazy są skalowane z zachowaniem proporcji, a następnie przycinane do docelowego rozmiaru.\n")
        info_text.insert(tk.END, "Wyższe wartości jakości i wyostrzania zapewniają lepsze rezultaty, ale zwiększają rozmiar plików.\n\n")
        info_text.insert(tk.END, "Obsługiwane formaty obrazów: JPG/JPEG, PNG, BMP, GIF, TIFF")
        info_text.config(state=tk.DISABLED)
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Wybierz folder z obrazami")
        if folder:
            self.input_folder.set(folder)
            # Automatycznie ustaw folder wyjściowy jako podfolder "resized" w folderze wejściowym
            if not self.output_folder.get():
                self.output_folder.set(os.path.join(folder, "resized"))
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Wybierz folder docelowy")
        if folder:
            self.output_folder.set(folder)
    
    def start_processing(self):
        # Sprawdź czy wybrano foldery
        if not self.input_folder.get():
            messagebox.showerror("Błąd", "Wybierz folder z obrazami!")
            return
        
        if not self.output_folder.get():
            messagebox.showerror("Błąd", "Wybierz folder docelowy!")
            return
        
        # Sprawdź czy wymiary są poprawne
        try:
            width = self.target_width.get()
            height = self.target_height.get()
            quality = self.quality.get()
            sharpen_factor = self.sharpen_factor.get()
            
            if width <= 0 or height <= 0:
                raise ValueError("Wymiary muszą być większe od zera")
            
            if quality < 0 or quality > 100:
                raise ValueError("Jakość musi być w zakresie 0-100")
            
            if sharpen_factor < 0:
                raise ValueError("Współczynnik wyostrzania musi być większy od zera")
        except:
            messagebox.showerror("Błąd", "Podaj poprawne wartości parametrów!")
            return
        
        # Rozpocznij przetwarzanie w osobnym wątku
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.progress.set(0)
        self.status_text.set("Rozpoczynam przetwarzanie...")
        
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()
    
    def process_images(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        target_width = self.target_width.get()
        target_height = self.target_height.get()
        quality = self.quality.get()
        sharpen_factor = self.sharpen_factor.get()
        
        # Sprawdź czy folder wyjściowy istnieje, jeśli nie - utwórz go
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # Obsługiwane formaty obrazów
        supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
        
        # Znajdź wszystkie obrazy w folderze wejściowym
        image_files = []
        for filename in os.listdir(input_folder):
            file_path = os.path.join(input_folder, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(supported_formats):
                image_files.append(filename)
        
        total_images = len(image_files)
        processed_images = 0
        
        if total_images == 0:
            self.root.after(0, lambda: messagebox.showinfo("Informacja", "Brak obrazów do przetworzenia w wybranym folderze!"))
            self.root.after(0, self.reset_ui)
            return
        
        # Przetwórz każdy obraz
        for i, filename in enumerate(image_files):
            if not self.processing:  # Sprawdź czy nie przerwano przetwarzania
                break
            
            file_path = os.path.join(input_folder, filename)
            
            try:
                # Aktualizuj status
                self.root.after(0, lambda f=filename: self.status_text.set(f"Przetwarzanie: {f}"))
                
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
                    else:
                        # Dla innych formatów użyj domyślnych ustawień
                        img_final.save(output_path, quality=quality, optimize=True)
                    
                    processed_images += 1
                    
                    # Aktualizuj pasek postępu
                    progress_value = (i + 1) / total_images * 100
                    self.root.after(0, lambda v=progress_value: self.progress.set(v))
                    
                    # Krótka pauza, aby UI mogło się zaktualizować
                    time.sleep(0.01)
            
            except Exception as e:
                error_msg = f"Błąd podczas przetwarzania {filename}: {e}"
                self.root.after(0, lambda msg=error_msg: self.status_text.set(msg))
                time.sleep(1)  # Daj czas na przeczytanie błędu
        
        # Zakończenie
        if self.processing:
            result_msg = f"Zakończono! Przetworzono {processed_images} z {total_images} obrazów."
            self.root.after(0, lambda: messagebox.showinfo("Sukces", result_msg))
            self.root.after(0, lambda msg=result_msg: self.status_text.set(msg))
        
        self.root.after(0, self.reset_ui)
    
    def reset_ui(self):
        self.processing = False
        self.process_button.config(state=tk.NORMAL)
    
    def on_closing(self):
        if self.processing:
            if messagebox.askyesno("Przerwać?", "Przetwarzanie w toku. Czy na pewno chcesz zamknąć aplikację?"):
                self.processing = False
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
