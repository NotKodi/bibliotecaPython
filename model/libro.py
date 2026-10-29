class Libro:
    def __init__(self, codigo, titulo,autor,anio,categoria, codigo_socio=None):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self-categoria=categoria
        self.codigo_socio = codigo_socio

    def __str__(self):
        return f"Código: {self.codigo}, {self.titulo}, {self.autor}, anio: {self.anio}"
    
    def __eq__(self,otro):
        if not isinstance(otro, Libro):
            return False
        return self.codigo == otro.codigo