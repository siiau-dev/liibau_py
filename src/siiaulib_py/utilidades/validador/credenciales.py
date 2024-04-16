from .base import _SIIAUValidadorBase

class _SIIAUValidadorCredenciales(_SIIAUValidadorBase):
    _expresiones = {
        'codigo': r'^\d{5}$|^\d{7,}$',
        'nip': r'^[a-zA-Z0-9]{1,10}$'
    }

    def valida_codigo(self, codigo: str):
        return self._valida('codigo', codigo)

    def valida_nip(self, nip: str):
        return self._valida('nip', nip)
