import json
import os

class ArchivoServicio:
    @staticmethod
    def guardar_datos(ruta_archivo: str, datos: list):
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        try:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error al guardar el archivo {ruta_archivo}: {e}")

    @staticmethod
    def cargar_datos(ruta_archivo: str) -> list:
        if not os.path.exists(ruta_archivo):
            return []
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar el archivo {ruta_archivo}: {e}")
            return []