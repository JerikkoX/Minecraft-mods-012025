import os
import requests
import zipfile
import shutil
import json
import tkinter as tk
from tkinter import messagebox

# URLs de descarga desde MEGA
MEGA_ZIP_GENERAL = "https://mega.nz/file/48dxgRAI#YmXBSS1IbG9qYednxHypoWfQkDmJMjAxZvb13Y1Tjfg"
MEGA_ZIP_MODS = "https://mega.nz/file/Jxs1yDSR#-j59s-53Cofh7Kj8qLgrSCz547pEwHUcb3gPVaDsRHU"
MODS_JSON_URL = "https://raw.githubusercontent.com/JerikkoX/Minecraft-mods-012025/main/mods_list.json"

# Rutas de instalación
MINECRAFT_PATH = os.path.expanduser("~") + "/AppData/Roaming/.minecraft/"
MODS_PATH = os.path.expanduser("~") + "/AppData/Roaming/.minecraft/installations/Minecraft 1.20.1 con mods 2025/mods/"
TEMP_PATH = "mods_temp/"

# Función para descargar archivos

def descargar_archivo(url, destino):
    print(f"Descargando {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destino, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print("Descarga completada.")
        return True
    else:
        print("Error en la descarga.")
        return False

# Función para extraer un ZIP

def extraer_zip(archivo_zip, destino):
    print(f"Extrayendo {archivo_zip} en {destino}...")
    with zipfile.ZipFile(archivo_zip, "r") as zip_ref:
        zip_ref.extractall(destino)
    print("Extracción completada.")

# Instalación de archivos generales

def instalar_archivos_generales():
    destino_zip = "general.zip"
    if descargar_archivo(MEGA_ZIP_GENERAL, destino_zip):
        extraer_zip(destino_zip, MINECRAFT_PATH)
        os.remove(destino_zip)
        messagebox.showinfo("Instalación", "Archivos generales instalados correctamente.")
    else:
        messagebox.showerror("Error", "No se pudieron instalar los archivos generales.")

# Instalación y actualización de mods

def obtener_lista_mods():
    try:
        response = requests.get(MODS_JSON_URL)
        if response.status_code == 200:
            return json.loads(response.text)["mods"]
    except Exception as e:
        print(f"Error al obtener la lista de mods: {e}")
    return []

def actualizar_mods():
    lista_mods = obtener_lista_mods()
    if not lista_mods:
        messagebox.showerror("Error", "No se pudo obtener la lista de mods.")
        return
    
    destino_zip = "mods.zip"
    if descargar_archivo(MEGA_ZIP_MODS, destino_zip):
        extraer_zip(destino_zip, TEMP_PATH)
        extracted_mods_path = os.path.join(TEMP_PATH, "mods")
        if os.path.exists(extracted_mods_path):
            if not os.path.exists(MODS_PATH):
                os.makedirs(MODS_PATH)
            
            for mod in os.listdir(MODS_PATH):
                if mod not in lista_mods:
                    os.remove(os.path.join(MODS_PATH, mod))
                    print(f"Eliminado mod obsoleto: {mod}")
            
            for mod in lista_mods:
                shutil.copy(os.path.join(extracted_mods_path, mod), MODS_PATH)
            
            shutil.rmtree(TEMP_PATH)
            os.remove(destino_zip)
            messagebox.showinfo("Actualización", "Mods actualizados correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró la carpeta de mods en el ZIP descargado.")
    else:
        messagebox.showerror("Error", "No se pudieron descargar los mods.")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Minecraft Mod Installer")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Minecraft Mod Installer", font=("Arial", 14)).pack(pady=10)
tk.Button(frame, text="Instalar Archivos Generales", command=instalar_archivos_generales, font=("Arial", 12)).pack(pady=5)
tk.Button(frame, text="Actualizar Mods", command=actualizar_mods, font=("Arial", 12)).pack(pady=5)
tk.Button(frame, text="Salir", command=root.quit, font=("Arial", 12)).pack(pady=10)

root.mainloop()
