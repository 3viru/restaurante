from model.bebida import Bebida

class BebidaImportada(Bebida):
    def __init__(self, id_item: int, nombre: str, precioBaseUSD: float, disponible: bool, esAlcoholica: bool, paisOrigen: str):
        super().__init__(id_item, nombre, precioBaseUSD, disponible, esAlcoholica)
        self.precioBaseUSD = precioBaseUSD
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

    def obtenerPrecioVenta(self, indExt: float = 1.0) -> float:
        return self.__precioBaseUSD * float(indExt)
