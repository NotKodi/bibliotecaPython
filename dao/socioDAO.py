from model.libro import Libro
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
                        
                        # Previo a guardar el socio verificamos si tiene un libro prestado, si no lo dejamos en none
                        codigo_libro = partes[3] if len(partes) > 3 and partes[3] != "" else None

                        socio = Socio(
                            codigo_socio=int(partes[0]),
                            nombre=partes[1],
                            email=partes[2],
                            codigo_libro_prestado=codigo_libro
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
                # Si codigo_libro_prestado es None, guardamos una cadena vacía
                libro_str = socio.codigo_libro_prestado if socio.codigo_libro_prestado is not None else ""
                
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