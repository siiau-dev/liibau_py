class _SIIAUParserInicio:
    def __init__(self, super_self):
        self._super_self = super_self

    def extraer_atributos_ocultos(self) -> dict[str, str]:
        atributos_elemento = {
            'type': 'hidden'
        }

        lista_atributos_elementos = self._super_self._extraer_elementos_crudos(
            'input',
            atributos_elemento
        )

        atributos_ocultos = {}

        if lista_atributos_elementos:
            for elemento in lista_atributos_elementos:
                atributos_ocultos[elemento['name']] = elemento['value']

        return atributos_ocultos

    def extraer_pidm(self) -> str:
        atributos = {
            'name': 'p_pidm_n'
        }

        elemento = self._super_self._extraer_elemento_crudo('input', atributos)

        return elemento['value'] if elemento else None

    _errores_inicio_sesion = {
        'credenciales_invalidas': "alert('Los datos proporcionados no son validos');",
        'usuario_bloqueado': "document.location.replace(\"gupuweb.bloqueo\");",
        'ingreso_no_valido': "alert(\"INGRESO NO VALIDO\");"
    }

    def extraer_error_inicio_sesion(self) -> str:
        cadena_error = self._super_self.extraer_elemento('script')

        if cadena_error:
            for tipo, error in self._errores_inicio_sesion.items():
                if cadena_error == error:
                    return tipo

        return 'error_desconocido'
