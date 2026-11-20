"""
entidad_miguel.py - Clase abstracta que representa las entidades del sistema.
Integrante responsable: Miguel Ángel Echeverría Caballero

Aquí está la base de todo: Cliente, Servicio y Reserva heredan de esta clase,
así todas comparten un identificador y la forma de mostrarse en pantalla.
"""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Base abstracta de Cliente, Servicio y Reserva.

    Es abstracta a propósito: no tiene sentido crear una "entidad" a secas,
    solo sus hijas concretas.
    """

    def __init__(self, identificador):
        # Guardamos el código único (ej. CLI-001, SRV-002, RES-003)
        self._identificador = identificador

    @property
    def identificador(self):
        """Solo lectura: una vez creada la entidad, su código no se puede cambiar."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Cada entidad explica cómo se describe a sí misma (polimorfismo).

        Las clases hijas están obligadas a implementarlo.
        """

    def __str__(self):
        # Así, al hacer print(entidad), se muestra su descripción directamente
        return self.describir()
