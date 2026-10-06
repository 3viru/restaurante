from model.detallepedido import DetallePedido
from model.item_sin_stock_error import ItemSinStockError
from model.pedido_cerrado_error import PedidoCerradoError

class Pedido:
    def __init__(self, numeroPedido: int, fechaHora: str):
        self.numeroPedido = numeroPedido
        self.__fechaHora = fechaHora
        self.__estado = "Abierto"
        self.__detalles = []

    @property
    def numeroPedido(self) -> int:
        return self.__numeroPedido

    @numeroPedido.setter
    def numeroPedido(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("El número de pedido debe ser un entero positivo.")
        self.__numeroPedido = int(valor)

    @property
    def fechaHora(self) -> str:
        return self.__fechaHora

    @property
    def detalles(self) -> list:
        return self.__detalles
    
    @property
    def estado(self) -> str:
        return self.__estado

    def agregarDetalle(self, item, cant: int, obs: str = "") -> DetallePedido:
        """
        Agrega una línea de detalle al pedido (Composición: crea DetallePedido dentro de Pedido;
        Agregación: recibe el ItemMenu preexistente).
        Lanza excepciones propias del dominio si se violan reglas del negocio.
        """
        if self.__estado != "Abierto":
            raise PedidoCerradoError(f"Regla de negocio: El pedido #{self.__numeroPedido} está cerrado y no admite más ítems.")
        if not item.verificarStockIngredientes():
            raise ItemSinStockError(f"Regla de negocio: El ítem '{item.nombre}' no tiene stock disponible.")
        
        detalle = DetallePedido(cant, obs, item)
        self.__detalles.append(detalle)
        return detalle

    def calcularTotal(self, indExt: float = 1.0) -> float:
        total = 0.0
        for d in self.__detalles:
            total += d.item.obtenerPrecioVenta(indExt) * d.cantidad
        return total

    def cerrarPedido(self) -> None:
        self.__estado = "Cerrado"
