import cv2
from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, Text
import os

def increase_saturation(img_pil, factor=1.5):
    """Aumenta la saturazione dell'immagine."""
    enhancer = ImageEnhance.Color(img_pil)
    return enhancer.enhance(factor)

def process_image(image_path, output_width=200, saturation_factor=1.5):
    """Aumenta la saturazione, converte in scala di grigi e genera l'arte ASCII."""
    img = cv2.imread(image_path)
    if img is None:
        print("Errore: Impossibile caricare l'immagine.")
        return None
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_pil = increase_saturation(img_pil, saturation_factor)
    img_pil = img_pil.convert("L")
    width, height = img_pil.size
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio * 0.5)
    img_pil = img_pil.resize((output_width, output_height))
    ascii_chars = " .:-=+*#%@"
    pixels = list(img_pil.getdata())
    ascii_image = ''.join(ascii_chars[pixel * (len(ascii_chars) - 1) // 255] for pixel in pixels)
    ascii_image = '\n'.join([ascii_image[i:i + output_width] for i in range(0, len(ascii_image), output_width)])
    return ascii_image

def save_ascii_art():
    """Funzione per salvare l'arte ASCII come file di testo."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        ascii_art = text_widget.get(1.0, tk.END).strip()
        if ascii_art:
            with open(file_path, 'w') as file:
                file.write(ascii_art)
            print(f"Arte ASCII salvata in: {file_path}")
        else:
            print("Errore: Nessun contenuto ASCII da salvare.")

def save_ascii_as_html():
    """Apre una finestra di dialogo per salvare l'arte ASCII come HTML."""
    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if file_path:
        ascii_art = text_widget.get(1.0, tk.END).strip()
        if ascii_art:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Arte ASCII</title>
                <style>
                    body {{
                        background-color: #2E3440;
                        color: #D8DEE9;
                        font-family: monospace;
                        white-space: pre-wrap;
                        padding: 20px;
                    }}
                </style>
            </head>
            <body>
                <pre>{ascii_art}</pre>
            </body>
            </html>
            """
            with open(file_path, 'w') as file:
                file.write(html_content)
            print(f"Arte ASCII salvata come HTML: {file_path}")
        else:
            print("Errore: Nessun contenuto ASCII da salvare.")

def open_image():
    """Apre una finestra di dialogo per selezionare l'immagine da convertire in ASCII."""
    file_path = filedialog.askopenfilename()
    if file_path:
        ascii_art = process_image(file_path)
        if ascii_art:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, ascii_art)
        else:
            print("Errore: Impossibile convertire l'immagine in arte ASCII.")

# Crea la finestra principale
root = tk.Tk()
root.title("ASCII Art Converter")

# Configura il layout della finestra principale
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Definisci la palette di colori
bg_color = "#2E3440"
fg_color = "#D8DEE9"
button_color = "#4C566A"
button_text_color = "#ECEFF4"
text_bg_color = "#3B4252"
text_fg_color = "#ECEFF4"

# Applica i colori alla finestra principale
root.configure(bg=bg_color)
                
# Crea un frame per i pulsanti
button_frame = tk.Frame(root, bg=bg_color)
button_frame.grid(row=0, column=0, pady=10)

# Crea un pulsante per aprire l'immagine
open_button = tk.Button(button_frame, text="Open Image", command=open_image, bg=button_color, fg=button_text_color)
open_button.grid(row=0, column=0, padx=5)

# Crea un pulsante per esportare l'arte ASCII come HTML
save_html_button = tk.Button(button_frame, text="Save as HTML", command=save_ascii_as_html, bg=button_color, fg=button_text_color)
save_html_button.grid(row=0, column=1, padx=5)

# Crea un widget di testo per visualizzare l'arte ASCII
text_widget = Text(root, wrap=tk.NONE, font=("Courier", 10), bg=text_bg_color, fg=text_fg_color)
text_widget.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Avvia il loop principale di tkinter
root.mainloop()
