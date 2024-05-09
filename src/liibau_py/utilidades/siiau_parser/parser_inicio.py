import re

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

    def extraer_planes(self):
        planes_estudio = []

        atributos_planes = {
            'name': 'p_carrera'
        }

        lista_planes_estudio = self._super_self._extraer_elemento_crudo(
            'select',
            atributos_planes
        )

        if lista_planes_estudio:
            for plan in lista_planes_estudio.find_all('option'):
                planes_estudio.append(plan.text)
                #planes_estudio.append(plan.text[:plan.text.index('-')])

        else:
            # Sólo hay un plan de estudios, lo sacamos de otra forma

            # Este validador lo ponemos aquí y no en siiau_validador por la
            # forma en la que funcionan los módulos en Python, igual esta
            # librería será obsoleta pronto
            validador_plan = re.compile(r'^sgpofer\.secciones')

            atributos_plan = {
                'href': validador_plan
            }

            elemento_plan_estudios = self._super_self._extraer_elemento_crudo(
                'a',
                atributos_plan
            )

            if not elemento_plan_estudios:
                # Manejaremos el error más delante
                return None

            # El plan de estudios se encuentra en un link, lo extraemos de
            # esta manera
            link_plan = elemento_plan_estudios.get('href')
            planes_estudio.append(link_plan[link_plan.index('majrp=') + 6:])

        # To do: Ordenar por orden cronológico
        # ... Para la siguiente librería
        return planes_estudio

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
