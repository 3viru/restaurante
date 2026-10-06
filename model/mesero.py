from model.trabajador import Trabajador

class Mesero(Trabajador):
    def __init__(self, rut: str, nombre: str):
        super().__init__(rut, nombre, "Mesero")

    def tomarPedido(self, mesa) -> object:
        pass

    def marcarMesa(self, mesa, estado: str) -> None:
        pass

    def tienePermiso(self, accion: str) -> bool:
        return accion in ["tomar_pedido", "ver_mesas"]
