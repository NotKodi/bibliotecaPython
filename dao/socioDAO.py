from model.socio import Socio
from .file_manager import FileManager


class SocioDAO(FileManager):

    def __init__(self):
        super().__init__("socios.txt")

    def leer_todos(self) -> list[Socio]:
        """Lee todos los socios del fichero."""
        socios = []
        file = self._abrir_fichero("r")

        if file:
            try:
                next(file, None)  # Salta la cabecera
                for linea in file:
                    if linea.strip():
                        partes = linea.strip().split("|")
                        val_libro = partes[3].strip() if len(partes) > 3 else ""
                        codigo_libro = (
                            None
                            if val_libro == "" or val_libro.upper() == "NONE"
                            else int(val_libro)
                        )

                        socio = Socio(
                            codigo_socio=int(partes[0]),
                            nombre=partes[1],
                            email=partes[2],
                            codigo_libro_prestado=codigo_libro,
                        )
                        socios.append(socio)
            except Exception as e:
                print(f"Error al procesar los socios: {e}")
            finally:
                file.close()

        return socios

    def create(self, socio: Socio) -> bool:
        """Añade un nuevo socio al final del fichero."""
        file = self._abrir_fichero("a")
        if file:
            try:
                libro_str = (
                    str(socio.codigo_libro_prestado)
                    if socio.codigo_libro_prestado is not None
                    else "NONE"
                )
                linea = f"{socio.codigo_socio}|{socio.nombre}|{socio.email}|{libro_str}\n"
                file.write(linea)
                print(f"Socio '{socio.nombre}' guardado correctamente.")
                return True
            except Exception as e:
                print(f"Error al escribir el socio: {e}")
                return False
            finally:
                file.close()
        return False

    def actualizar_prestamo(
        self, codigo_socio: int, codigo_libro: int | None
    ) -> bool:
        #Modifica el valor de codigo_libro_prestado para permitir devolver o prestar.
        socios = self.leer_todos()
        socio_encontrado = False

        for socio in socios:
            if socio.codigo_socio == codigo_socio:
                socio.codigo_libro_prestado = codigo_libro
                socio_encontrado = True
                break

        if not socio_encontrado:
            return False

        file = self._abrir_fichero("w")
        if file:
            try:
                file.write("codigo_socio|nombre|email|codigo_libro_prestado\n")
                for socio in socios:
                    libro_str = (
                        str(socio.codigo_libro_prestado)
                        if socio.codigo_libro_prestado is not None
                        else "NONE"
                    )
                    file.write(
                        f"{socio.codigo_socio}|{socio.nombre}|{socio.email}|{libro_str}\n"
                    )
                return True
            except Exception as e:
                print(f"Error al actualizar el socio: {e}")
                return False
            finally:
                file.close()
        return False