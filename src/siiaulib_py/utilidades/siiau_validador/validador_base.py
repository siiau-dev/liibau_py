import re

class _SIIAUValidadorBase:
    def _valida(self, expresion: str, cadena: str) -> bool:
        if expresion not in self._expresiones:
            raise ValueError(f"No se encontró una expresión regular para "
                                "{expresion}")

        return bool(re.match(self._expresiones[expresion], cadena))
