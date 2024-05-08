from .error_base import _SIIAUErrorBase

class SIIAUErrorInicioSesion(_SIIAUErrorBase):
    def __init__(self, tipo: str, contenido: str = None, *args) -> None:
        self.tipo = tipo
        super().__init__(tipo, *args)
