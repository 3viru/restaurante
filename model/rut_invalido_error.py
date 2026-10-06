class RutInvalidoError(Exception):
    """Excepción de negocio lanzada cuando un RUT de cliente no supera la validación del algoritmo Módulo 11."""
    def __init__(self, mensaje: str = "El RUT ingresado no es válido según el algoritmo Módulo 11."):
        super().__init__(mensaje)
