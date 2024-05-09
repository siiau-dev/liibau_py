from .enlaces_base import _EnlacesBaseSIIAU

class _EnlacesAlumnoSIIAU(_EnlacesBaseSIIAU):
    _enlaces = {
        # Inicio de sesión
        'inicio_paso1': "/wus/gupprincipal.forma_inicio",
        'inicio_paso2': "/wus/gupprincipal.forma_inicio_bd",
        'inicio_paso3': "/wus/GUPPRINCIPAL.VALIDA_INICIO",

        # Planes de estudio
        'planes': "/wal/gupmenug.menu",
    }
