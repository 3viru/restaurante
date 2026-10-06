from model.itemmenu import ItemMenu

class PlatoCaliente(ItemMenu):
    def __init__(self, id_item: int, nombre: str, precioBase: float, disponible: bool, temperaturaServicio: int):
        super().__init__(id_item, nombre, precioBase, disponible)
        self.temperaturaServicio = temperaturaServicio

    @property
    def temperaturaServicio(self) -> int:
        return self.__temperaturaServicio

    @temperaturaServicio.setter
    def temperaturaServicio(self, valor: int):
        if int(valor) < 0:
            raise ValueError("La temperatura de servicio no puede ser menor a 0°C.")
        self.__temperaturaServicio = int(valor)

    @property
    def estacion(self) -> str:
        return "Cocina Caliente"

    def preparar(self, estacion: str) -> None:
        pass

    def obtenerTiempoPreparacion(self) -> int:
        return 20

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.precioBase
