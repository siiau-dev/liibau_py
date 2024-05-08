import re

class _SIIAUValidadorBase:
    def _revisar_expresion(self, expresion: str):
        if expresion not in self._expresiones:
            raise ValueError(f"No se encontró una expresión regular para "
                                "{expresion}")

    def _valida(self, expresion: str, cadena: str) -> bool:
        self._revisar_expresion(expresion)
        return bool(re.match(self._expresiones[expresion], cadena))

    def _validador(self, expresion: str):
        self._revisar_expresion(expresion)
        return re.compile(self._expresiones[expresion])
