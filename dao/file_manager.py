import os
from errores import error_formato, error_no_encontrado, error_permisos


class FileManager:

    def __init__(self, filename: str, base_path: str = "data"):
        self.filepath = os.path.join(base_path, filename)

    def _abrir_fichero(self, modo: str = "r"):
        """Abre el fichero o lanza la excepción correspondiente."""
        try:
            file = open(self.filepath, modo, encoding="utf-8")
            print(f"Fichero '{self.filepath}' abierto correctamente ({modo}).")
            return file
        except FileNotFoundError:
            raise error_no_encontrado(self.filepath)
        except (PermissionError, OSError):
            raise error_permisos(self.filepath, modo)