import os
import requests
import zipfile
import shutil
import json
import tkinter as tk
from tkinter import messagebox

# Configuración
GITHUB_ZIP_URL = "https://mega.nz/fm/xsNT2T4R"
MODS_LIST_URL = "https://github.com/JerikkoX/Minecraft-mods-012025/blob/main/mods_list.json"
SCRIPT_URL = "https://raw.githubusercontent.com/JerikkoX/Minecraft-mods-012025/main/instalar_mods.py"

MINECRAFT_PATH = os.path.expanduser("~") + "/AppData/Roaming/.minecraft/version2/"
MODS_PATH = MINECRAFT_PATH + "mods/"
TEMP_PATH = "mods_temp/"

def descargar_mods():
    """ Descarga el ZIP de los mods desde GitHub """
    print("Descargando mods desde GitHub...")
    response = requests.get(GITHUB_ZIP_URL, stream=True)
    
    if response.status_code == 200:
        with open("mods.zip", "wb") as file:
            file.write(response.content)
        print("Descarga completa.")
    else:
        print("Error al descargar los mods.")
        return False
    return True

def extraer_mods():
    """ Extrae los mods descargados """
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)

    with zipfile.ZipFile("mods.zip", "r") as zip_ref:
        zip_ref.extractall(TEMP_PATH)
    
    repo_name = os.listdir(TEMP_PATH)[0]  # Nombre del repo extraído
    extracted_mods_path = os.path.join(TEMP_PATH, repo_name, "mods")

    if not os.path.exists(extracted_mods_path):
        print("No se encontró la carpeta de mods en el repositorio.")
        return False
    
    return extracted_mods_path

def obtener_lista_mods():
    """ Descarga la lista de mods desde GitHub """
    try:
        response = requests.get(MODS_LIST_URL)
        if response.status_code == 200:
            return json.loads(response.text)["mods"]
        else:
            print("Error al obtener la lista de mods.")
            return []
    except Exception as e:
        print(f"Error al descargar la lista de mods: {e}")
        return []

def limpiar_mods_antiguos(lista_mods):
    """ Elimina versiones antiguas y mods que no están en GitHub """
    if not os.path.exists(MODS_PATH):
        os.makedirs(MODS_PATH)

    mods_actuales = os.listdir(MODS_PATH)
    
    # Borrar mods no existentes en GitHub
    for mod in mods_actuales:
        if mod not in lista_mods:
            os.remove(os.path.join(MODS_PATH, mod))
            print(f"Eliminado mod extra: {mod}")

    # Borrar versiones antiguas
    for mod_nuevo in lista_mods:
        base_name = mod_nuevo.rsplit("-", 1)[0]  # Ejemplo: "neko-mod"
        for mod_viejo in mods_actuales:
            if mod_viejo.startswith(base_name) and mod_viejo != mod_nuevo:
                os.remove(os.path.join(MODS_PATH, mod_viejo))
                print(f"Eliminado mod antiguo: {mod_viejo}")

def instalar_mods(extracted_mods_path, lista_mods):
    """ Instala solo los mods que están en la lista de GitHub """
    for mod in lista_mods:
        shutil.copy(os.path.join(extracted_mods_path, mod), MODS_PATH)
    print("Mods instalados correctamente.")

def limpiar():
    """ Limpia archivos temporales """
    if os.path.exists("mods.zip"):
        os.remove("mods.zip")
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)

def actualizar_mods():
    """ Función principal para actualizar los mods """
    if descargar_mods():
        mods_path = extraer_mods()
        if mods_path:
            lista_mods = obtener_lista_mods()
            if lista_mods:
                limpiar_mods_antiguos(lista_mods)
                instalar_mods(mods_path, lista_mods)
    limpiar()
    messagebox.showinfo("Actualización", "Mods actualizados correctamente.")

def actualizar_script():
    """ Descarga y ejecuta el script más reciente desde GitHub """
    try:
        response = requests.get(SCRIPT_URL)
        if response.status_code == 200:
            with open("instalar_mods.py", "w") as file:
                file.write(response.text)
            os.system("python instalar_mods.py")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el script.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al actualizar el script: {e}")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Actualizador de Mods")

tk.Label(root, text="Minecraft Mod Updater", font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Actualizar Mods", command=actualizar_mods, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Actualizar Programa", command=actualizar_script, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Salir", command=root.quit, font=("Arial", 12)).pack(pady=10)

root.mainloop()