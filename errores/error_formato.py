class DataFormatError(Exception):
    """Se lanza cuando una línea del fichero no se puede convertir al modelo."""

    def __init__(self, linea: str, detalle: str = ""):
        self.linea = linea
        super().__init__(
            f"Formato de datos incorrecto en la línea: '{linea.strip()}'. {detalle}"
        )