class EnlacesBaseSIIAU:
    _base_url = "siiauescolar.siiau.udg.mx"

    def _construir_enlace(self, ruta, metodo = None, base = None):
        if not base:
            base = self._base_url

        if not metodo:
            metodo = 'https'

        return f"{metodo}://{base}{ruta}"

    def construir_enlace(self, tipo: str, *args, **kwargs) -> str:
        if tipo not in self._enlaces:
            raise ValueError(f"No se encuentra el enlace {tipo}")

        return self._construir_enlace(
            self._enlaces[tipo],
            *args,
            **kwargs
        )
