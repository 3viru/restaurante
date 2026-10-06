from model.trabajador import Trabajador

class Cocinero(Trabajador):
    def __init__(self, rut: str, nombre: str, estacionAsignada: str):
        super().__init__(rut, nombre, "Cocinero")
        self.__estacionAsignada = estacionAsignada

    def prepararItem(self, detalle) -> None:
        pass

    def marcarComoListo(self, detalle) -> None:
        pass

    def tienePermiso(self, accion: str) -> bool:
        return accion in ["ver_pedidos", "preparar_items"]
