class FileNotFoundAppError(Exception):
    """Se lanza cuando el fichero no existe en la ruta especificada."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        super().__init__(f"El fichero no existe en la ruta: '{filepath}'")