class PedidoCerradoError(Exception):
    """Excepción de negocio lanzada cuando se intenta agregar ítems o modificar un pedido que ya está cerrado."""
    def __init__(self, mensaje: str = "No es posible agregar ítems ni modificar un pedido cerrado."):
        super().__init__(mensaje)
