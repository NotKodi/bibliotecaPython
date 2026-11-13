from model.libro import Libro
from dao.file_manager import FileManager


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

                        # Extraemos el valor de codigo_socio y limpiamos espacios
                        val_socio = partes[5].strip() if len(partes) > 5 else ""

                        # Si en el .txt pone "NONE" o está vacío, en Python es None
                        if val_socio == "" or val_socio.upper() == "NONE":
                            codigo_socio = None
                        else:
                            codigo_socio = int(val_socio)

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

    def leer_disponibles(self) -> list[Libro]:
        todos = self.leer_todos()
        return [libro for libro in todos if libro.codigo_socio is None]

    def crear(self, libro: Libro) -> bool:
        file = self._abrir_fichero("a")
        if file:
            try:
                # Si codigo_socio es None, guardamos "NONE" para mantener el formato de tu .txt
                socio_str = str(libro.codigo_socio) if libro.codigo_socio is not None else "NONE"

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

    def actualizar_todos(self, libros: list[Libro]) -> bool:
        file = self._abrir_fichero("w")
        if file:
            try:
                file.write("codigo|titulo|autor|anio|categoria|codigo_socio\n")
                for libro in libros:
                    socio_str = str(libro.codigo_socio) if libro.codigo_socio is not None else "NONE"
                    file.write(
                        f"{libro.codigo}|{libro.titulo}|{libro.autor}|{libro.anio}|{libro.categoria}|{socio_str}\n"
                    )
                return True
            except Exception as e:
                print(f"Error al actualizar los libros: {e}")
                return False
            finally:
                file.close()
        return False