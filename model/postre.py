from model.itemmenu import ItemMenu

class Postre(ItemMenu):
    def __init__(self, id_item: int, nombre: str, precioBase: float, disponible: bool, requiereRefrigeracion: bool):
        super().__init__(id_item, nombre, precioBase, disponible)
        self.requiereRefrigeracion = requiereRefrigeracion

    @property
    def requiereRefrigeracion(self) -> bool:
        return self.__requiereRefrigeracion

    @requiereRefrigeracion.setter
    def requiereRefrigeracion(self, valor: bool):
        self.__requiereRefrigeracion = bool(valor)

    @property
    def estacion(self) -> str:
        return "Cocina Fría"

    def obtenerTiempoPreparacion(self) -> int:
        return 10

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.precioBase
