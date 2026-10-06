from model.itemmenu import ItemMenu

class Bebida(ItemMenu):
    def __init__(self, id_item: int, nombre: str, precioBase: float, disponible: bool, esAlcoholica: bool):
        super().__init__(id_item, nombre, precioBase, disponible)
        self.esAlcoholica = esAlcoholica

    @property
    def esAlcoholica(self) -> bool:
        return self.__esAlcoholica

    @esAlcoholica.setter
    def esAlcoholica(self, valor: bool):
        self.__esAlcoholica = bool(valor)

    @property
    def estacion(self) -> str:
        return "Barra"

    def preparar(self, estacion: str) -> None:
        pass

    def obtenerTiempoPreparacion(self) -> int:
        return 5

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.precioBase
