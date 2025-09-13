import tkinter as tk
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import cv2
import sys
import os
import time

def mostrar_texto(ruta, frame):
    try:
        with open(ruta, "r") as f:
            contenido = f.read(10000)  # lee máximo 10k chars para no colgar
        label = tk.Label(frame, text=contenido, justify="left", anchor="nw")
        label.pack(fill="both", expand=True)
    except Exception as e:
        tk.Label(frame, text=f"Error mostrando texto:\n{e}").pack()


def mostrar_imagen(ruta, frame):
    try:
        img = Image.open(ruta)
        img.thumbnail((800, 600))  # escalado rápido y liviano
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(frame, image=tk_img)
        label.image = tk_img
        label.pack()
    except Exception as e:
        tk.Label(frame, text=f"Error mostrando imagen:\n{e}").pack()


def mostrar_pdf(ruta, frame):
    try:
        pages = convert_from_path(ruta, dpi=100, first_page=1, last_page=1)
        img = pages[0]
        img.thumbnail((800, 600))
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(frame, image=tk_img)
        label.image = tk_img
        label.pack()
    except Exception as e:
        tk.Label(frame, text=f"Error mostrando PDF:\n{e}").pack()


def mostrar_video(ruta, frame):
    try:
        cap = cv2.VideoCapture(ruta)
        label = tk.Label(frame)
        label.pack()

        def reproducir():
            ret, frame_img = cap.read()
            if ret:
                frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
                img = ImageTk.PhotoImage(Image.fromarray(frame_img))
                label.config(image=img)
                label.image = img
                frame.after(33, reproducir)  # ~30 fps
            else:
                cap.release()

        reproducir()
    except Exception as e:
        tk.Label(frame, text=f"Error mostrando video:\n{e}").pack()


def centrar_ventana(root):
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"+{x}+{y}")


def quicksee(path):
    root = tk.Tk()
    root.title("QuickSee Optimizado")
    root.overrideredirect(True)  # sin bordes

    # cerrar rápido
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-3>", lambda e: root.destroy())

    frame = tk.Frame(root)
    frame.pack()

    ext = path.lower()
    if ext.endswith(".txt"):
        mostrar_texto(path, frame)
    elif ext.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
        mostrar_imagen(path, frame)
    elif ext.endswith(".pdf"):
        mostrar_pdf(path, frame)
    elif ext.endswith((".mp4", ".avi", ".mov", ".mkv")):
        mostrar_video(path, frame)
    else:
        tk.Label(frame, text="⚠️ Formato no soportado").pack()

    root.after(100, lambda: centrar_ventana(root))
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python quicksee.py <ruta_del_archivo>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        if not os.path.isfile(file_path):
            print("Archivo no válido")
            sys.exit(1)
        quicksee(file_path)