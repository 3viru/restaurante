from model.mesa_ocupada_error import MesaOcupadaError

class Mesa:
    def __init__(self, numero: int, capacidad: int, estado: str = "Disponible", tienePedidoAbierto: bool = False):
        self.numero = numero
        self.capacidad = capacidad
        self.__estado = str(estado)
        self.__tienePedidoAbierto = bool(tienePedidoAbierto)

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

    @estado.setter
    def estado(self, valor: str):
        if not valor or not str(valor).strip():
            raise ValueError("El estado de la mesa no puede estar vacío.")
        self.__estado = str(valor).strip()

    @property
    def tienePedidoAbierto(self) -> bool:
        return self.__tienePedidoAbierto

    @tienePedidoAbierto.setter
    def tienePedidoAbierto(self, valor: bool):
        self.__tienePedidoAbierto = bool(valor)

    def abrirMesa(self) -> bool:
        """Abre la mesa para un pedido. Lanza MesaOcupadaError si la regla de negocio lo impide."""
        if self.__estado == "Ocupada" or self.__tienePedidoAbierto:
            raise MesaOcupadaError(f"Regla de negocio: La mesa N°{self.__numero} ya está ocupada con un pedido activo.")
        self.__estado = "Ocupada"
        self.__tienePedidoAbierto = True
        return True

    def cerrarMesa(self) -> None:
        self.__estado = "Disponible"
        self.__tienePedidoAbierto = False
