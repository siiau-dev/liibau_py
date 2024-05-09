from .error_base import _SIIAUErrorBase

class SIIAUErrorPeticion(_SIIAUErrorBase):
    def __init__(self, tipo: str, contenido: str = None, *args) -> None:
        self.tipo = tipo
        self.contenido = contenido
        super().__init__(tipo, *args)
