class Socio:
    def __init__(self, codigo_socio, nombre, email, codigo_libro_prestado = None):
        self.codigo_socio = codigo_socio
        self.nombre = nombre
        self.email = email
        self.codigo_libro_prestado = codigo_libro_prestado


    def __str__(self):
        if self.codigo_libro_prestado != None:
            return f"Socio {self.codigo_socio}, nombre: {self.nombre}, email: {self.email}, libro prestado: {self.codigo_libro_prestado} "
        else:
            return f"Socio {self.codigo_socio}, nombre: {self.nombre}, email: {self.email} "
    
    def __eq__(self,otro):
        if not isinstance(otro, Socio):
            return False
        return self.codigo_socio == otro.codigo_socio