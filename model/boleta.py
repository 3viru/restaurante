from model.rut_invalido_error import RutInvalidoError

class Boleta:
    def __init__(self, numeroBoleta: int, rutCliente: str, montoNeto: float):
        self.numeroBoleta = numeroBoleta
        self.rutCliente = rutCliente
        self.montoNeto = montoNeto

    @property
    def numeroBoleta(self) -> int:
        return self.__numeroBoleta

    @numeroBoleta.setter
    def numeroBoleta(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("El número de boleta debe ser un entero positivo.")
        self.__numeroBoleta = int(valor)

    @property
    def rutCliente(self) -> str:
        return self.__rutCliente

    @rutCliente.setter
    def rutCliente(self, rut: str):
        if not self.validarRut(rut):
            raise RutInvalidoError(f"El RUT '{rut}' no es válido según el algoritmo Módulo 11.")
        self.__rutCliente = rut

    @property
    def montoNeto(self) -> float:
        return self.__montoNeto

    @montoNeto.setter
    def montoNeto(self, valor: float):
        if float(valor) < 0:
            raise ValueError("El monto neto no puede ser negativo.")
        self.__montoNeto = float(valor)
        self.__montoTotal = round(self.__montoNeto * 1.19, 2)

    @property
    def montoTotal(self) -> float:
        return self.__montoTotal

    @staticmethod
    def validarRut(rut: str) -> bool:
        if not rut or not isinstance(rut, str):
            return False
        limpio = rut.replace(".", "").replace("-", "").strip()
        if len(limpio) < 8 or len(limpio) > 9:
            return False
        cuerpo = limpio[:-1]
        dv = limpio[-1].upper()
        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2
        for d in reversed(cuerpo):
            suma += int(d) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        dv_esperado = 11 - resto
        if dv_esperado == 11:
            calc_dv = "0"
        elif dv_esperado == 10:
            calc_dv = "K"
        else:
            calc_dv = str(dv_esperado)

        return dv == calc_dv

    def emitirBoleta(self) -> bool:
        """Emite la boleta verificando que el RUT del cliente sea válido."""
        if not self.validarRut(self.__rutCliente):
            raise RutInvalidoError(f"Regla de negocio: No se puede emitir boleta con RUT inválido: {self.__rutCliente}")
        return True
