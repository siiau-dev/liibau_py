from copy import deepcopy
from .__utils__ import SIIAUtils

class AlumnoSIIAU:
    def __init__(self, codigo: str, nip: str,
            auto_refrecar_sesion: bool = True):
        self._requester = SIIAUtils.requester.SIIAURequester()
        self._auto_refresco = auto_refrecar_sesion

        validador = SIIAUtils.validador.SIIAUValidador.inicio_sesion
        if not validador.valida_codigo(codigo):
            raise SIIAUtils.errores.SIIAUErrorInicioSesion(
                'codigo_formato_incorrecto'
            )

        if not validador.valida_nip(nip):
            raise SIIAUtils.errores.SIIAUErrorInicioSesion(
                'nip_formato_incorrecto'
            )

        self._codigo = codigo if self._auto_refresco else None
        self._nip = nip if self._auto_refresco else None


        # Creamos la sesión en cuanto se crea el objeto
        self.renovar_sesion(codigo, nip)
        self._conseguir_planes()

    def _peticion(self, *args, **kwargs):
        # Todo: implementar lógica para cuando la sesión explira
        respuesta = self._requester.hacer_peticion(*args, **kwargs)
        self._actualizar_expiracion()
        return respuesta

    def _actualizar_expiracion(self):
        # Todo: Revisar cuánto tarda en expirar la sesión
        pass

    def renovar_sesion(self, codigo: str = None, nip: str = None):
        if (not self._auto_refresco) and \
                (codigo is None or nip is None):
            raise Exception("No es posible renovar la sesión sin"
                    "credenciales.")

        enlaces = SIIAUtils.enlaces.EnlacesSIIAU.alumno
        parser = SIIAUtils.parser.SIIAUParser

        payload = {
            'p_codigo_c': codigo if codigo else self._codigo,
            'p_clave_c': nip if nip else self._nip
        }

        paso_1 = self._peticion(
            tipo = 'GET',
            url = enlaces.construir_enlace('inicio_paso1'),
            inicio_sesion = True
        )

        parser_paso_1 = parser(paso_1.text)
        payload_paso_2 = deepcopy(payload)
        payload_paso_2.update(parser_paso_1.inicio.extraer_atributos_ocultos())

        # Esta respuesta no es necesaria actualmente
        _paso_2 = self._peticion(
            tipo = 'POST',
            url = enlaces.construir_enlace('inicio_paso2'),
            payload = payload_paso_2,
            inicio_sesion = True
        )

        paso_3 = self._peticion(
            tipo = 'POST',
            url = enlaces.construir_enlace('inicio_paso3'),
            payload = payload,
            inicio_sesion = True
        )

        parser_paso_3 = parser(paso_3.text)

        self._pidm = parser_paso_3.inicio.extraer_pidm()
        # No necesitamos hacer nada con las cookies, esas ya están
        # almacenadas en nuestro requester

        if not self._pidm:
            # Hubo un error al iniciar sesión
            error = parser_paso_3.inicio.extraer_error_inicio_sesion()
            raise SIIAUtils.errores.SIIAUErrorPeticion(error, paso_3.text)

    def _conseguir_planes(self):
        enlaces = SIIAUtils.enlaces.EnlacesSIIAU.alumno
        parser = SIIAUtils.parser.SIIAUParser

        payload = {
            'p_sistema_c': 'ALUMNOS',
            'p_sistemaid_n': 3,
            'p_menupredid_n': 3,
            'p_pidm_n': self._pidm
        }

        respuesta = self._peticion(
            tipo = 'POST',
            url = enlaces.construir_enlace('planes'),
            payload = payload
        )

        parser_planes = parser(respuesta.text)
        self._planes_estudio = parser_planes.inicio.extraer_planes()

        # Teóricamente esto no debería pasar
        if not self._planes_estudio:
            raise SIIAUtils.errores.SIIAUErrorInicioSesion(
                'no_planes_estudio'
            )

    # Agregamos propiedades para que el usuario sepa que no debe modificarlas

    @property
    def pidm(self):
        return self._pidm

    @pidm.setter
    def pidm(self, *args, **kwargs):
        # Agregar SIIAUError
        raise Exception("No es posible editar el pidm de un alumno. "
                "Crea una nueva sesión.")

    @property
    def cookies(self):
        return self._requester._sesion.cookies.get_dict()

    @cookies.setter
    def cookies(self, *args, **kwargs):
        # Agregar SIIAUError
        raise Exception("No es posible editar las cookies de un alumno. "
                "Crea una nueva sesión.")

    @property
    def planes_estudio(self):
        return self._planes_estudio

    @planes_estudio.setter
    def planes_estudio(self, *args, **kwargs):
        # Agregar SIIAUError
        raise Exception("No es posible cambiar los planes de estudio de un "
                "alumno. Crea una nueva sesión.")
