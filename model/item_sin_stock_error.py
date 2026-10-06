class ItemSinStockError(Exception):
    """Excepción de negocio lanzada cuando un ítem no tiene stock suficiente para ser agregado a un pedido."""
    def __init__(self, mensaje: str = "El ítem seleccionado no cuenta con stock disponible."):
        super().__init__(mensaje)
