class Usuario:
    def __init__(self, identificacion: str, nombre: str):
        self.identificacion = identificacion
        self.nombre = nombre

    def a_diccionario(self) -> dict:
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre
        }

    @classmethod
    def desde_diccionario(cls, datos: dict):
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"]
        )