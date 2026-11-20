from enum import Enum

from cliente_miguel import Cliente
from entidad_miguel import Entidad
from excepciones_eva import (CalculoInconsistenteError, OperacionNoPermitidaError,
                         ParametroFaltanteError, ParametroInvalidoError,
                         ReservaInvalidaError, ServicioNoDisponibleError)
from registro_eva import obtener_logger
from servicio_miguel import Servicio

logger = obtener_logger()


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"


class Reserva(Entidad):
    """Integra cliente, servicio, duración y estado."""

    def __init__(self, identificador, cliente, servicio, horas):
        super().__init__(identificador)
        try:
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("El cliente no es válido")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("El servicio no es válido")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {servicio.identificador} no está disponible")
            servicio.validar_parametros(horas)
        except (ParametroInvalidoError, ParametroFaltanteError,
                ServicioNoDisponibleError) as error:
            # Encadenamiento: la causa original queda en __cause__
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva {identificador}") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = EstadoReserva.PENDIENTE
        self._costo_total = None
        logger.info("Reserva %s creada: %s -> %s (%s h)", identificador,
                    cliente.nombre, servicio.nombre, horas)

    def confirmar(self):
        """Pendiente -> Confirmada. Usa try/finally."""
        try:
            if self._estado != EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva {self._estado.value.lower()}")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {self._servicio.identificador} fue bloqueado")
            self._estado = EstadoReserva.CONFIRMADA
            logger.info("Reserva %s confirmada", self.identificador)
        finally:
            # Se ejecuta siempre, haya o no error
            logger.debug("Intento de confirmar %s terminado (estado: %s)",
                         self.identificador, self._estado.value)

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada."""
        if self._estado in (EstadoReserva.PROCESADA, EstadoReserva.CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado.value.lower()}")
        self._estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada", self.identificador)

    def procesar(self, impuesto=None, descuento=None):
        """Confirmada -> Procesada. Usa try/except/else/finally."""
        try:
            if self._estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    "Solo se procesan reservas confirmadas "
                    f"(estado actual: {self._estado.value})")
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            logger.error("Fallo al procesar %s: %s", self.identificador, error)
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva {self.identificador}") from error
        else:
            # Solo si el try terminó sin errores
            self._costo_total = costo
            self._estado = EstadoReserva.PROCESADA
            logger.info("Reserva %s procesada. Total: $%s", self.identificador,
                        f"{costo:,.2f}")
            return costo
        finally:
            logger.debug("Procesamiento de %s terminado", self.identificador)

    def describir(self):
        total = f", total ${self._costo_total:,.2f}" if self._costo_total else ""
        return (f"Reserva {self.identificador} [{self._estado.value}] "
                f"{self._cliente.nombre} -> {self._servicio.nombre} "
                f"({self._horas} h){total}")
