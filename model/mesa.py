from model.mesa_ocupada_error import MesaOcupadaError

class Mesa:
    def __init__(self, numero: int, capacidad: int):
        self.numero = numero
        self.capacidad = capacidad
        self.__estado = "Libre"
        self.__tienePedidoAbierto = False

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, valor: int):
        if valor <= 0:
            raise ValueError("El número de mesa debe ser un entero positivo.")
        self.__numero = valor

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if valor <= 0:
            raise ValueError("La capacidad de la mesa debe ser mayor a 0 personas.")
        self.__capacidad = valor

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def tienePedidoAbierto(self) -> bool:
        return self.__tienePedidoAbierto

    def abrirMesa(self) -> bool:
        """Abre la mesa para un pedido. Lanza MesaOcupadaError si la regla de negocio lo impide."""
        if self.__estado == "Ocupada" or self.__tienePedidoAbierto:
            raise MesaOcupadaError(f"Regla de negocio: La mesa N°{self.__numero} ya está ocupada con un pedido activo.")
        self.__estado = "Ocupada"
        self.__tienePedidoAbierto = True
        return True

    def cerrarMesa(self) -> None:
        self.__estado = "Libre"
        self.__tienePedidoAbierto = False
