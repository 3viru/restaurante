from model.itemmenu import ItemMenu

class DetallePedido:
    def __init__(self, cantidad: int, observacion: str, item: ItemMenu):
        self.cantidad = cantidad
        self.observacion = observacion
        self.__item = item
        self.__listo = False

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("La cantidad de ítems debe ser un número entero mayor a 0.")
        self.__cantidad = int(valor)

    @property
    def observacion(self) -> str:
        return self.__observacion

    @observacion.setter
    def observacion(self, valor: str):
        self.__observacion = str(valor) if valor is not None else ""

    @property
    def item(self) -> ItemMenu:
        return self.__item

    @property
    def listo(self) -> bool:
        return self.__listo

    def marcarPreparado(self) -> None:
        self.__listo = True
