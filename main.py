from dao.libroDAO import LibroDAO
from dao.log_manager import LogManager
from dao.socioDAO import SocioDAO
from errores.error_formato import DataFormatError
from errores.error_no_encontrado import FileNotFoundAppError
from errores.error_permisos import FileAccessError
from model.libro import Libro
from model.socio import Socio


class Main:

    def __init__(
        self,
        libro_dao: LibroDAO,
        socio_dao: SocioDAO,
        log_manager: LogManager,
    ):
        self.libro_dao = libro_dao
        self.socio_dao = socio_dao
        self.log_manager = log_manager
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
        self.log_manager.registrar("INICIO_APP", "Sesión iniciada en la biblioteca")

        while not self.salir:
            self.mostrar_menu()
            try:
                self.opcion = int(input("Seleccione una de las opciones (1-8): "))
            except ValueError:
                print("ERROR: Valor no válido, intente de nuevo.")
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
                    self.log_manager.registrar("FIN_APP", "Sesión finalizada por el usuario")
                    print("Hasta luego")
                    self.salir = True
                else:
                    print("Opción fuera de rango (1-8).")

            except (FileNotFoundAppError, FileAccessError, DataFormatError) as e:
                self.log_manager.registrar("ERROR_FICHERO", str(e))
                print(f"Fallo en el fichero o datos: {e}")
            except Exception as e:
                self.log_manager.registrar("ERROR_INESPERADO", str(e))
                print(f"Error inesperado: {e}")

    def _opcion_1_mostrar_todos_libros(self):
        libros = self.libro_dao.leer_todos()
        self.log_manager.registrar(
            "READ_LIBROS", f"Consulta de todos los libros ({len(libros)} encontrados)"
        )
        if not libros:
            print("No hay libros registrados.")
            return
        print("== TODOS LOS LIBROS ==")
        for libro in libros:
            print(libro)

    def _opcion_2_mostrar_libros_disponibles(self):
        libros = self.libro_dao.leer_disponibles()
        self.log_manager.registrar(
            "READ_DISPONIBLES",
            f"Consulta de libros disponibles ({len(libros)} encontrados)",
        )
        if not libros:
            print("No hay libros disponibles actualmente.")
            return
        print("== LIBROS DISPONIBLES ==")
        for libro in libros:
            print(libro)

    def _opcion_3_buscar_libro(self):
        termino = input("Ingrese el título o término a buscar: ").strip()
        if not termino:
            print("Debe introducir un término de búsqueda.")
            return

        libros = self.libro_dao.leer_todos()
        encontrados = [
            l for l in libros if termino.lower() in l.titulo.lower()
        ]

        if encontrados:
            self.log_manager.registrar(
                "BUSCAR_LIBRO",
                f"Búsqueda por término '{termino}': {len(encontrados)} coincidencia(s)",
            )
            print(f"\n== RESULTADOS PARA '{termino}' ==")
            for libro in encontrados:
                print(libro)
        else:
            self.log_manager.registrar(
                "BUSCAR_LIBRO",
                f"Búsqueda sin resultados para el término '{termino}'",
            )
            print(f"No se encontraron libros que contengan '{termino}'.")

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
        if socio.codigo_libro_prestado is not None:
            print(
                f"El socio ya tiene prestado el libro {socio.codigo_libro_prestado}."
            )
            return

        # 1. Actualizamos el libro y reescribimos libros.txt
        libro.codigo_socio = socio.codigo_socio
        self.libro_dao.actualizar_todos(libros)

        # 2. Actualizamos el socio en socios.txt
        self.socio_dao.actualizar_prestamo(socio.codigo_socio, libro.codigo)

        # 3. Registramos en el log
        self.log_manager.registrar(
            "PRESTAMO",
            f"Libro '{libro.titulo}' (Cód: {libro.codigo}) prestado a '{socio.nombre}' (Cód: {socio.codigo_socio})",
        )
        print(f"Libro '{libro.titulo}' prestado a '{socio.nombre}'.")

    def _opcion_5_devolver_libro(self):
        try:
            cod_l = int(input("Código del libro a devolver: "))
        except ValueError:
            print("Código no válido.")
            return

        libros = self.libro_dao.leer_todos()
        libro = next((l for l in libros if l.codigo == cod_l), None)

        if not libro or libro.codigo_socio is None:
            print("El libro no existe o no está prestado.")
            return

        cod_socio_anterior = libro.codigo_socio

        # 1. Liberamos el libro y actualizamos libros.txt
        libro.codigo_socio = None
        self.libro_dao.actualizar_todos(libros)

        # 2. Quitamos el libro del socio en socios.txt
        self.socio_dao.actualizar_prestamo(cod_socio_anterior, None)

        # 3. Registramos en el log
        self.log_manager.registrar(
            "DEVOLUCION",
            f"Libro '{libro.titulo}' (Cód: {libro.codigo}) devuelto por el socio Cód: {cod_socio_anterior}",
        )
        print(f"Libro '{libro.titulo}' devuelto correctamente.")

    def _opcion_6_mostrar_socios_con_prestamo(self):
        socios = self.socio_dao.leer_todos()
        con_prestamo = [s for s in socios if s.codigo_libro_prestado is not None]

        self.log_manager.registrar(
            "READ_PRESTAMOS",
            f"Consulta de socios con préstamo activo ({len(con_prestamo)} encontrados)",
        )

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
                if self.libro_dao.crear(nuevo_l):
                    self.log_manager.registrar(
                        "CREATE_LIBRO", f"Nuevo libro: '{tit}' (Cód: {cod})"
                    )

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
                if self.socio_dao.create(nuevo_s):
                    self.log_manager.registrar(
                        "CREATE_SOCIO", f"Nuevo socio: '{nom}' (Cód: {cod_s})"
                    )
            else:
                print("Opción no válida.")
        except ValueError:
            print("Tipo de dato incorrecto.")


def main():
    libro_dao = LibroDAO()
    socio_dao = SocioDAO()
    log_manager = LogManager()

    app = Main(libro_dao, socio_dao, log_manager)
    app.seleccion_menu()


if __name__ == "__main__":
    main()