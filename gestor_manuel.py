from cliente_miguel import Cliente
from excepciones_eva import (ClienteInvalidoError, ParametroFaltanteError,
                         ParametroInvalidoError, ReservaInvalidaError,
                         ServicioNoDisponibleError)
from registro_eva import obtener_logger
from reserva_manuel import Reserva
from servicio_miguel import Asesoria, AlquilerEquipo, ReservaSala

logger = obtener_logger()

# Tipos de servicio que el sistema sabe crear
TIPOS_SERVICIO = {"sala": ReservaSala, "equipo": AlquilerEquipo,
                  "asesoria": Asesoria}


class GestorSoftwareFJ:
    """Controla clientes, servicios y reservas en listas en memoria."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, **datos):
        """Registra un cliente. Usa try/except/else con encadenamiento."""
        try:
            nuevo = Cliente(f"CLI-{len(self.clientes) + 1:03d}", **datos)
            # Regla de negocio: el documento no puede repetirse
            if any(c.documento == nuevo.documento for c in self.clientes):
                raise ClienteInvalidoError("Ya existe un cliente con ese documento",
                                           detalle=nuevo.documento)
        except (ParametroFaltanteError, ParametroInvalidoError, TypeError) as error:
            logger.warning("Registro de cliente rechazado: %s", error)
            raise ClienteInvalidoError("No fue posible registrar el cliente") from error
        else:
            self.clientes.append(nuevo)     # Solo se agrega si no hubo errores
            logger.info("Cliente registrado: %s", nuevo)
            return nuevo

    def registrar_servicio(self, tipo, **datos):
        """Crea un servicio del tipo indicado. Usa try/except/else."""
        try:
            clase = TIPOS_SERVICIO.get(tipo)
            if clase is None:
                raise ParametroInvalidoError(
                    f"Tipo de servicio desconocido. Use: {', '.join(TIPOS_SERVICIO)}",
                    detalle=tipo)
            nuevo = clase(f"SRV-{len(self.servicios) + 1:03d}", **datos)
        except TypeError as error:
            # Se envió un parámetro que la clase no conoce
            raise ParametroInvalidoError("Parámetros de servicio incorrectos") from error
        else:
            self.servicios.append(nuevo)
            logger.info("Servicio registrado: %s", nuevo)
            return nuevo

    def _buscar(self, lista, identificador, error):
        """Busca una entidad por identificador o lanza el error indicado."""
        for elemento in lista:
            if elemento.identificador == identificador:
                return elemento
        raise error("No encontrado", detalle=identificador)

    def buscar_cliente(self, identificador):
        return self._buscar(self.clientes, identificador, ClienteInvalidoError)

    def buscar_servicio(self, identificador):
        return self._buscar(self.servicios, identificador, ServicioNoDisponibleError)

    def buscar_reserva(self, identificador):
        return self._buscar(self.reservas, identificador, ReservaInvalidaError)

    def crear_reserva(self, id_cliente, id_servicio, horas):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        reserva = Reserva(f"RES-{len(self.reservas) + 1:03d}", cliente, servicio, horas)
        self.reservas.append(reserva)
        return reserva
