import os


class FileManager:
    """Clase base para la gestión directa y apertura de ficheros."""

    def __init__(self, filename: str, base_path: str = "data"):
        self.filepath = os.path.join(base_path, filename)

    def _abrir_fichero(self, modo: str = "r"):
        """Intenta abrir el fichero y devuelve el objeto file si tiene éxito."""
        try:
            file = open(self.filepath, modo, encoding="utf-8")
            print(f"Fichero '{self.filepath}' abierto correctamente ({modo}).")
            return file
        except FileNotFoundError:
            print(f"Error: El fichero '{self.filepath}' no existe.")
        except Exception as e:
            print(f"Error al abrir '{self.filepath}': {e}")
        return None