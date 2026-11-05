from model.libro import Libro
from model.socio import Socio
from .file_manager import FileManager


class LibroDAO(FileManager):

    def __init__(self):
        super().__init__("libros.txt")

    def leer_todos(self) -> list[Libro]:
        libros = []
        file = self._abrir_fichero("r")

        if file:
            try:
                next(file, None)  # Salta la cabecera
                for linea in file:
                    if linea.strip():
                        partes = linea.strip().split("|")
                        
                        #Vemos si el libro está prestado, si no dejamos el campo vacío
                        codigo_socio = partes[5] if len(partes) > 5 and partes[5] != "" else None

                        libro = Libro(
                            codigo=int(partes[0]),
                            titulo=partes[1],
                            autor=partes[2],
                            anio=int(partes[3]),
                            categoria=partes[4],
                            codigo_socio=codigo_socio
                        )
                        libros.append(libro)
            except Exception as e:
                print(f"Error al procesar los libros: {e}")
            finally:
                file.close()

        return libros

    def crear(self, libro: Libro) -> bool:
        """Añade un nuevo libro al final del fichero."""
        file = self._abrir_fichero("a")
        if file:
            try:
                # Si codigo_socio es None, guardamos una cadena vacía
                socio_str = libro.codigo_socio if libro.codigo_socio is not None else ""
                
                # Formato delimitado por '|'
                linea = f"{libro.codigo}|{libro.titulo}|{libro.autor}|{libro.anio}|{libro.categoria}|{socio_str}\n"
                file.write(linea)
                print(f"Libro '{libro.titulo}' guardado correctamente.")
                return True
            except Exception as e:
                print(f"Error al escribir el libro: {e}")
                return False
            finally:
                file.close()
        return False


