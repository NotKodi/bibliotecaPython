from errores.error_formato import DataFormatError
from errores.error_permisos import FileAccessError
from errores.error_no_encontrado import FileNotFoundAppError
from dao.libroDAO import LibroDAO
from dao.socioDAO import SocioDAO
from model.libro import Libro
from model.socio import Socio


class Main:

    def __init__(self, libro_dao: LibroDAO, socio_dao: SocioDAO):
        self.libro_dao = libro_dao
        self.socio_dao = socio_dao
        self.opcion = None
        self.salir = False

    def mostrar_menu(self):
        print("\n== BIBLIOTECA PYTHON BY KODI ==")
        print("1. Mostrar todos los libros")
        print("2. Mostrar libros disponibles")
        print("3. Buscar un libro")
        print("4. Prestar libro a socio")
        print("5. Devolver libro")
        print("6. Mostrar socios por libro prestado")
        print("7. Añadir socios y libros")
        print("8. Finalizar")

    def seleccion_menu(self):
        while not self.salir:
            self.mostrar_menu()
            try:
                self.opcion = int(input("Seleccione una de las opciones (1-8): "))
            except ValueError:
                print("RROR: Valor no válido, intente de nuevo")
                continue

            try:
                if self.opcion == 1:
                    self._opcion_1_mostrar_todos_libros()
                elif self.opcion == 2:
                    self._opcion_2_mostrar_libros_disponibles()
                elif self.opcion == 3:
                    self._opcion_3_buscar_libro()
                elif self.opcion == 4:
                    self._opcion_4_prestar_libro()
                elif self.opcion == 5:
                    self._opcion_5_devolver_libro()
                elif self.opcion == 6:
                    self._opcion_6_mostrar_socios_con_prestamo()
                elif self.opcion == 7:
                    self._opcion_7_anadir_socio_o_libro()
                elif self.opcion == 8:
                    print("Hasta luego")
                    self.salir = True
                else:
                    print("Opción fuera de rango (1-8).")

            except (FileNotFoundAppError, FileAccessError, DataFormatError) as e:
                print(f"Fallo en el fichero o datos: {e}")
            except Exception as e:
                print(f"Error inesperado: {e}")


    def _opcion_1_mostrar_todos_libros(self):
        libros = self.libro_dao.leer_todos()
        if not libros:
            print("No hay libros registrados.")
            return
        print("==TODOS LOS LIBROS==")
        for libro in libros:
            print(libro)

    def _opcion_2_mostrar_libros_disponibles(self):
        # Usamos tu método directo del DAO
        libros = self.libro_dao.leer_disponibles()
        if not libros:
            print("No hay libros disponibles actualmente.")
            return
        print("==LIBROS DISPONIBLES==")
        for libro in libros:
            print(libro)

    def _opcion_3_buscar_libro(self):
        try:
            codigo = int(input("Ingrese código del libro: "))
        except ValueError:
            print("El código debe ser numérico.")
            return

        libros = self.libro_dao.leer_todos()
        encontrado = next((l for l in libros if l.codigo == codigo), None)

        if encontrado:
            print(f"Libro encontrado: {encontrado}")
        else:
            print(f"No existe un libro con código {codigo}.")

    def _opcion_4_prestar_libro(self):
        try:
            cod_l = int(input("Código del libro: "))
            cod_s = int(input("Código del socio: "))
        except ValueError:
            print("Los códigos deben ser enteros.")
            return

        libros = self.libro_dao.leer_todos()
        socios = self.socio_dao.leer_todos()

        libro = next((l for l in libros if l.codigo == cod_l), None)
        socio = next((s for s in socios if s.codigo_socio == cod_s), None)

        if not libro:
            print("El libro no existe.")
            return
        if not socio:
            print("El socio no existe.")
            return
        if libro.codigo_socio is not None:
            print(f"El libro ya está prestado al socio {libro.codigo_socio}.")
            return

        # Actualizar relaciones en memoria
        libro.codigo_socio = socio.codigo_socio
        socio.codigo_libro_prestado = libro.codigo

        # Persistir cambios
        self.libro_dao.actualizar_todos(libros)
        self.socio_dao.actualizar_todos(socios)
        print(f"Libro '{libro.titulo}' prestado a '{socio.nombre}'.")

    def _opcion_5_devolver_libro(self):
        try:
            cod_l = int(input("Código del libro a devolver: "))
        except ValueError:
            print("Código no válido.")
            return

        libros = self.libro_dao.leer_todos()
        socios = self.socio_dao.leer_todos()

        libro = next((l for l in libros if l.codigo == cod_l), None)

        if not libro or libro.codigo_socio is None:
            print("El libro no existe o no está prestado.")
            return

        # Desvincular socio
        socio = next(
            (
                s
                for s in socios
                if str(s.codigo_libro_prestado) == str(libro.codigo)
            ),
            None,
        )

        libro.codigo_socio = None
        if socio:
            socio.codigo_libro_prestado = None

        self.libro_dao.actualizar_todos(libros)
        self.socio_dao.actualizar_todos(socios)
        print(f"Libro '{libro.titulo}' devuelto correctamente.")

    def _opcion_6_mostrar_socios_con_prestamo(self):
        socios = self.socio_dao.leer_todos()
        con_prestamo = [s for s in socios if s.codigo_libro_prestado is not None]

        if not con_prestamo:
            print("No hay socios con libros prestados.")
            return
        print("\n--- SOCIOS CON LIBROS PRESTADOS ---")
        for socio in con_prestamo:
            print(socio)

    def _opcion_7_anadir_socio_o_libro(self):
        print("1. Añadir Libro")
        print("2. Añadir Socio")
        opc = input("Opción: ").strip()

        try:
            if opc == "1":
                cod = int(input("Código: "))
                tit = input("Título: ").strip()
                aut = input("Autor: ").strip()
                anio = int(input("Año: "))
                cat = input("Categoría: ").strip()

                nuevo_l = Libro(
                    codigo=cod,
                    titulo=tit,
                    autor=aut,
                    anio=anio,
                    categoria=cat,
                    codigo_socio=None,
                )
                self.libro_dao.crear(nuevo_l)

            elif opc == "2":
                cod_s = int(input("Código Socio: "))
                nom = input("Nombre: ").strip()
                em = input("Email: ").strip()

                nuevo_s = Socio(
                    codigo_socio=cod_s,
                    nombre=nom,
                    email=em,
                    codigo_libro_prestado=None,
                )
                self.socio_dao.crear(nuevo_s)
            else:
                print("Opción no válida.")
        except ValueError:
            print("Tipo de dato incorrecto.")


def main():
    libro_dao = LibroDAO()
    socio_dao = SocioDAO()

    app = Main(libro_dao, socio_dao)
    app.seleccion_menu()


if __name__ == "__main__":
    main()