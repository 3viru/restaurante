class MesaOcupadaError(Exception):
    """Excepción de negocio lanzada cuando se intenta abrir una mesa que ya está ocupada o con pedido activo."""
    def __init__(self, mensaje: str = "La mesa ya se encuentra ocupada con un pedido activo."):
        super().__init__(mensaje)
