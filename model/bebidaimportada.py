from model.bebida import Bebida

class BebidaImportada(Bebida):
    def __init__(self, id_item: int, nombre: str, precioBase: float = 0.0, disponible: bool = True, esAlcoholica: bool = False, paisOrigen: str = "", precioBaseUSD: float = None):
        valor_usd = float(precioBaseUSD) if precioBaseUSD is not None else float(precioBase)
        super().__init__(id_item, nombre, valor_usd, disponible, esAlcoholica)
        self.precioBaseUSD = valor_usd
        self.paisOrigen = paisOrigen

    @property
    def paisOrigen(self) -> str:
        return self.__paisOrigen

    @paisOrigen.setter
    def paisOrigen(self, valor: str):
        if not valor or not str(valor).strip():
            raise ValueError("El país de origen no puede estar vacío.")
        self.__paisOrigen = str(valor).strip()

    @property
    def precioBaseUSD(self) -> float:
        return self.__precioBaseUSD

    @precioBaseUSD.setter
    def precioBaseUSD(self, valor: float):
        if float(valor) <= 0:
            raise ValueError("El precio base en USD debe ser mayor a 0.")
        self.__precioBaseUSD = float(valor)
        Bebida.precioBase.fset(self, float(valor))

    @Bebida.precioBase.setter
    def precioBase(self, valor: float):
        if float(valor) <= 0:
            raise ValueError("El precio base en USD debe ser mayor a 0.")
        Bebida.precioBase.fset(self, float(valor))
        self.__precioBaseUSD = float(valor)

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.__precioBaseUSD * float(indExt)
