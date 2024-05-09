from os import path
import sys

directorio_padre = path.abspath(__file__)
for _ in range(2):
    directorio_padre = path.dirname(directorio_padre)

modulo_utilidades = path.join(directorio_padre, "utilidades")
sys.path.append(modulo_utilidades)

import siiau_utils as SIIAUtils
__all__ = ['SIIAUtils']
