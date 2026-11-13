import os
from datetime import datetime
from dao.file_manager import FileManager


class LogManager(FileManager):
    """Clase para gestionar la lectura y escritura de logs del sistema."""

    def __init__(self):
        # Por defecto FileManager apunta a data/log.txt
        super().__init__("log.txt")

    def registrar(self, evento: str, detalles: str) -> bool:
        """Crea log.txt si no existe y añade la línea con el formato [Fecha][evento][detalles]."""
        # 1. Verificar si existe la carpeta y el fichero log.txt; si no, crearlo
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8"):
                pass  # Crea el fichero vacío

        # 2. Añadir el log pertinente al final del fichero
        file = self._abrir_fichero("a")
        if file:
            try:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                linea = f"[{fecha}][{evento}][{detalles}]\n"
                file.write(linea)
                return True
            except Exception as e:
                print(f"Error al escribir en el log: {e}")
                return False
            finally:
                file.close()
        return False

    def leer_todos(self) -> list[str]:
        """Lee y devuelve todas las líneas registradas en el log."""
        if not os.path.exists(self.filepath):
            return []

        logs = []
        file = self._abrir_fichero("r")
        if file:
            try:
                for linea in file:
                    if linea.strip():
                        logs.append(linea.strip())
            except Exception as e:
                print(f"Error al leer el log: {e}")
            finally:
                file.close()
        return logs