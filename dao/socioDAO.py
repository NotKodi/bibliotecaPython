from model.libro import Libro
from model.socio import Socio
from .file_manager import FileManager

class SocioDAO(FileManager):
    """DAO para operaciones CRUD de la entidad Socio sobre fichero."""

    def __init__(self):
        super().__init__("socios.txt")

    def read_all(self) -> list[Socio]:
        """Lee todos los socios del fichero."""
        socios = []
        file = self._abrir_fichero("r")

        if file:
            try:
                next(file, None)  # Salta la cabecera
                for linea in file:
                    if linea.strip():
                        partes = linea.strip().split("|")
                        socio = Socio(
                            id=int(partes[0]), 
                            nombre=partes[1], 
                            email=partes[2]
                        )
                        socios.append(socio)
            except Exception as e:
                print(f"Error al procesar los socios: {e}")
            finally:
                file.close()

        return socios