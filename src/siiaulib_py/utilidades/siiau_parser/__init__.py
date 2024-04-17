from bs4 import BeautifulSoup
from .parser_inicio import _SIIAUParserInicio

class SIIAUParser:
    def __init__(self, contenido: str, tipo: str = None) -> None:
        self._contenido = contenido
        self._tipo = tipo if tipo else 'html.parser'

        self._soup = BeautifulSoup(self._contenido, self._tipo)

        # Métodos específicos
        self.inicio = _SIIAUParserInicio(self)

    def _extraer_elementos_crudos(self, etiqueta_elemento: str,
            atributos: dict = None):
        if not atributos:
            atributos = {}

        lista_elementos = self._soup.find_all(etiqueta_elemento, atributos)
        return lista_elementos if lista_elementos else None

    def _extraer_elemento_crudo(self, etiqueta_elemento: str,
            atributos: dict = None):
        lista_elementos = self._extraer_elementos_crudos(etiqueta_elemento, atributos)
        return lista_elementos[0] if lista_elementos else None

    def extraer_elemento(self, etiqueta_elemento: str,
            atributos: dict = None) -> str:
        elemento = self._extraer_elemento_crudo(etiqueta_elemento, atributos)
        return elemento.string if elemento else None
