class FileAccessError(Exception):
    """Se lanza cuando ocurren problemas de permisos o bloqueos en el fichero."""

    def __init__(self, filepath: str, modo: str):
        self.filepath = filepath
        self.modo = modo
        super().__init__(
            f"Error al intentar acceder al fichero '{filepath}' en modo '{modo}'."
        )