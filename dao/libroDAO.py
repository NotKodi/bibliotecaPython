from model.libro import Libro
from model.socio import Socio
from .file_manager import FileManager


class LibroDAO(FileManager):
    """DAO para operaciones CRUD de la entidad Libro sobre fichero."""

    def __init__(self):
        super().__init__("libros.txt")

    def read_all(self) -> list[Libro]:
        """Lee todos los libros del fichero."""
        libros = []
        file = self._abrir_fichero("r")

        if file:
            try:
                next(file, None)  # Salta la cabecera
                for linea in file:
                    if linea.strip():
                        partes = linea.strip().split("|")
                        libro = Libro(
                            id=int(partes[0]),
                            titulo=partes[1],
                            autor=partes[2],
                            año=int(partes[3]),
                        )
                        libros.append(libro)
            except Exception as e:
                print(f"Error al procesar los libros: {e}")
            finally:
                file.close()

        return libros


