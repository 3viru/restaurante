class ItemMenu:
    def __init__(self, id_item: int, nombre: str, precioBase: float, disponible: bool):
        self.id = id_item
        self.nombre = nombre
        self.precioBase = precioBase
        self.disponible = disponible

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, value: str):
        if not value or not str(value).strip():
            raise ValueError("El nombre del ítem del menú no puede estar vacío.")
        self.__nombre = str(value).strip()

    @property
    def precioBase(self) -> float:
        return self.__precioBase

    @precioBase.setter
    def precioBase(self, value: float):
        if float(value) <= 0:
            raise ValueError("El precio base debe ser un valor positivo mayor a 0.")
        self.__precioBase = float(value)

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, value: bool):
        self.__disponible = bool(value)

    def verificarStockIngredientes(self) -> bool:
        return self.__disponible

    def preparar(self, estacion: str) -> None:
        pass

    def obtenerTiempoPreparacion(self) -> int:
        return 0

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.__precioBase
