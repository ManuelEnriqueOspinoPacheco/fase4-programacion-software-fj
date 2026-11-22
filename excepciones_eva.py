
class SoftwareFJError(Exception):
    """Clase base para las excepciones personalizadas del sistema Software FJ."""

    codigo = "FJ-000"

    def __init__(self, mensaje="Error general en Software FJ", detalle=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.detalle = detalle

    def __str__(self):
        """Devuelve el error con su código y detalle, si existe."""
        texto = f"[{self.codigo}] {self.mensaje}"

        if self.detalle:
            texto += f" ({self.detalle})"

        return texto


class ClienteInvalidoError(SoftwareFJError):
    """Error relacionado con clientes inválidos, duplicados o inexistentes."""
    codigo = "FJ-101"


class ParametroInvalidoError(SoftwareFJError):
    """Error cuando un parámetro tiene un valor o tipo incorrecto."""
    codigo = "FJ-102"


class ParametroFaltanteError(SoftwareFJError):
    """Error cuando falta un dato obligatorio."""
    codigo = "FJ-103"


class ServicioNoDisponibleError(SoftwareFJError):
    """Error cuando el servicio no existe o no está disponible."""
    codigo = "FJ-201"


class ReservaInvalidaError(SoftwareFJError):
    """Error cuando una reserva no cumple las condiciones necesarias."""
    codigo = "FJ-301"


class OperacionNoPermitidaError(SoftwareFJError):
    """Error cuando se intenta realizar una operación no permitida."""
    codigo = "FJ-302"


class CalculoInconsistenteError(SoftwareFJError):
    """Error cuando se detectan inconsistencias en los cálculos de costos."""
    codigo = "FJ-401"
