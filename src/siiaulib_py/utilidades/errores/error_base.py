import json
from os import path

directorio = path.dirname(path.abspath(__file__))
with open(path.join(directorio, 'mensajes_error.json')) \
        as archivo_mensajes_error:
    mensajes_error = json.load(archivo_mensajes_error)

class _SIIAUErrorBase(Exception):
    def __init__(self, tipo: str, *args) -> None:
      global mensajes_error

      if tipo not in mensajes_error:
          tipo = 'error_desconocido'

      super().__init__(mensajes_error[tipo], *args)
