class Libro:
    def __init__(self, codigo, titulo,autor,anio,categoria, codigo_socio=None):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self.categoria=categoria
        self.codigo_socio = codigo_socio

    def __str__(self):
        base = f"Código: {self.codigo}, {self.titulo} ({self.autor}, {self.anio}) - [{self.categoria}]"
        if self.codigo_socio is not None:
            return f"{base}, Prestado a: {self.codigo_socio}"
        return f"{base}"
    
    def __eq__(self,otro):
        if not isinstance(otro, Libro):
            return False
        return self.codigo == otro.codigo