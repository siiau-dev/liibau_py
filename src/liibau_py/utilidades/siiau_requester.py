import platform
from os import path
from requests import Session

from siiau_parser import SIIAUParser
from siiau_errores import SIIAUErrorPeticion


directorio_padre = path.abspath(__file__)
for _ in range(2):
    directorio_padre = path.dirname(directorio_padre)

info = {}
with open(path.join(directorio_padre, "__info__.py"), 'r') as f:
    exec(f.read(), info)

# Intentamos ser buenos usuarios del internet, por eso asignamos
# un user agent propio para que la UdeG pueda identificar las
# peticiones hechas con nuestras librerías.
#
# Si alguien de la UdeG está viendo esto, por favor no bloqueen
# nuestro user agent, sino nos tendremos que ver en la necesidad
# de utilizar user agents al azar de navegadores modernos para
# que nuestras librerías sigan funcionando.
#
# En ustedes está llevar el juego en paz.

FORMATO_USER_AGENT = "{nombre_lib} {version_lib} " \
                        "({sistema} {version} {arquitectura})"

class SIIAURequester:
    def __init__(self, sesion: Session = None):
        if sesion:
            self._sesion = sesion
        else:
            self._sesion = Session()

            user_agent = FORMATO_USER_AGENT.format(
                nombre_lib = info['__title__'],
                version_lib = info['__version__'],
                sistema = platform.uname()[0],
                version = platform.uname()[2],
                arquitectura = platform.uname()[4]
            )

            self._sesion.headers.update(
                {
                    'User-Agent' : user_agent
                }
            )

    def _extraer_sesion(self):
        return self._sesion

    def _peticion(self, *args, **kwargs):
        try:
            respuesta = self._sesion.request(*args, **kwargs)
            return respuesta
        except:
            return None

    def _hay_internet(self, url_a_probar: str = None):
        if not url_a_probar:
            url_a_probar = "https://www.google.com"
        url_siiau = "https://siiau.udg.mx"

        # Si no podemos entrar a la url por alguna razón pero sí a SIIAU
        # asumimos que podemos continuar.
        internet = self._peticion('GET', url_a_probar) is not None
        conexion_a_siiau = self._peticion('GET', url_siiau) is not None

        return True if internet else conexion_a_siiau

    def hacer_peticion(self, tipo: str, url: str, payload = None,
            inicio_sesion: bool = False):
        if not self._hay_internet():
            raise SIIAUErrorPeticion('no_internet')

        respuesta = self._peticion(
            method = tipo,
            url = url,
            data = payload
        )

        if respuesta is None or not respuesta.ok:
            raise SIIAUErrorPeticion('siiau_caido')

        if not inicio_sesion:
            # Todo: Revisar si la sesión aún es válida
            pass

        return respuesta
