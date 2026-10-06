class Trabajador:
    def __init__(self, rut: str, nombre: str, rol: str):
        self.rut = rut
        self.nombre = nombre
        self.__rol = rol

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        if not valor or not str(valor).strip():
            raise ValueError("El RUT del trabajador no puede estar vacío.")
        self.__rut = str(valor).strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not str(valor).strip():
            raise ValueError("El nombre del trabajador no puede estar vacío.")
        self.__nombre = str(valor).strip()

    @property
    def rol(self) -> str:
        return self.__rol

    def iniciarSesion(self) -> bool:
        return True

    def tienePermiso(self, accion: str) -> bool:
        return False
