"""
servicio_miguel.py - Clase abstracta Servicio y tres servicios especializados.
Integrante responsable: Miguel Ángel Echeverría Caballero

Servicio define lo común (nombre, tarifa, disponibilidad y cálculo del costo)
y cada servicio concreto (sala, equipo, asesoría) pone sus propias reglas.
"""
from abc import abstractmethod

from entidad_miguel import Entidad
from excepciones_eva import (CalculoInconsistenteError, ParametroFaltanteError,
                         ParametroInvalidoError)
from registro_eva import obtener_logger

# Logger compartido para dejar rastro de lo que pasa en el archivo de registro
logger = obtener_logger()


class Servicio(Entidad):
    """Clase abstracta de la que heredan todos los servicios."""

    IVA_DEFECTO = 0.19          # Impuesto por defecto (19 %)
    DESCUENTO_MAXIMO = 0.50     # Ningún descuento puede superar el 50 %

    def __init__(self, identificador, nombre=None, tarifa_hora=None):
        super().__init__(identificador)
        # El nombre es obligatorio y no puede ser solo espacios
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("Falta el nombre del servicio")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = self._validar_positivo(tarifa_hora, "tarifa por hora")
        # Todo servicio nuevo nace disponible
        self._disponible = True

    @staticmethod
    def _validar_positivo(valor, campo):
        """Valida que el valor sea un número mayor que cero."""
        if valor is None:
            raise ParametroFaltanteError(f"Falta el dato '{campo}'")
        # En Python True/False cuentan como int, por eso excluimos los booleanos
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ParametroInvalidoError(f"'{campo}' debe ser numérico", detalle=valor)
        if valor <= 0:
            raise ParametroInvalidoError(f"'{campo}' debe ser mayor que cero",
                                         detalle=valor)
        return valor

    @staticmethod
    def _validar_horas(horas, maximo):
        """Valida que la duración sea positiva y no supere el máximo."""
        Servicio._validar_positivo(horas, "duración (horas)")
        if horas > maximo:
            raise ParametroInvalidoError(
                f"La duración máxima permitida es {maximo} horas", detalle=horas)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def bloquear(self):
        """Marca el servicio como no disponible (ya no se podrá reservar)."""
        self._disponible = False
        logger.warning("Servicio %s bloqueado", self.identificador)

    @abstractmethod
    def calcular_costo_base(self, horas):
        """Costo sin impuestos ni descuentos (cada servicio lo sobrescribe)."""

    @abstractmethod
    def validar_parametros(self, horas):
        """Valida los parámetros propios de cada servicio (p. ej. horas máximas)."""

    def calcular_costo(self, horas, impuesto=None, descuento=None):
        """
        Método sobrecargado mediante parámetros opcionales
        (Python no tiene sobrecarga como tal, así que se simula así):
          calcular_costo(horas)                      -> con IVA por defecto
          calcular_costo(horas, impuesto)            -> con impuesto propio
          calcular_costo(horas, impuesto, descuento) -> con impuesto y descuento
        """
        try:
            # Primero revisamos las reglas propias del servicio
            self.validar_parametros(horas)
            # Si no nos pasan impuesto o descuento, usamos los valores por defecto
            impuesto = self.IVA_DEFECTO if impuesto is None else impuesto
            descuento = 0.0 if descuento is None else descuento
            # Ambos se manejan como fracciones: 0.19 = 19 %
            if not 0 <= impuesto <= 1:
                raise CalculoInconsistenteError("Impuesto fuera de rango [0, 1]",
                                                detalle=impuesto)
            if not 0 <= descuento <= self.DESCUENTO_MAXIMO:
                raise CalculoInconsistenteError(
                    f"Descuento fuera de rango [0, {self.DESCUENTO_MAXIMO}]",
                    detalle=descuento)
            # Orden del cálculo: costo base -> se aplica descuento -> se suma el impuesto
            total = self.calcular_costo_base(horas) * (1 - descuento) * (1 + impuesto)
            return round(total, 2)
        except (ParametroInvalidoError, ParametroFaltanteError, TypeError) as error:
            # Encadenamiento: se conserva la causa original (raise ... from ...)
            # para saber exactamente qué dato provocó el problema
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo de '{self.nombre}'") from error

    @abstractmethod
    def describir(self):
        """Descripción del servicio (polimorfismo)."""


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""
    MAX_HORAS = 12

    def __init__(self, identificador, nombre=None, tarifa_hora=None, capacidad=None):
        super().__init__(identificador, nombre, tarifa_hora)
        # La capacidad debe ser un número positivo; se guarda como entero
        self._capacidad = int(self._validar_positivo(capacidad, "capacidad"))

    def validar_parametros(self, horas):
        self._validar_horas(horas, self.MAX_HORAS)

    def calcular_costo_base(self, horas):
        costo = self.tarifa_hora * horas
        # Salas de más de 20 personas: 10 % de recargo
        return costo * 1.10 if self._capacidad > 20 else costo

    def describir(self):
        return (f"Sala {self.identificador} '{self.nombre}' para "
                f"{self._capacidad} personas, ${self.tarifa_hora:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos."""
    MAX_HORAS = 72
    COSTO_SEGURO = 5000     # Seguro fijo del equipo

    def __init__(self, identificador, nombre=None, tarifa_hora=None,
                 equipo=None, unidades=None):
        super().__init__(identificador, nombre, tarifa_hora)
        # Hay que indicar qué tipo de equipo se alquila (laptop, proyector, etc.)
        if equipo is None or not str(equipo).strip():
            raise ParametroFaltanteError("Falta el tipo de equipo")
        self._equipo = str(equipo).strip()
        self._unidades = int(self._validar_positivo(unidades, "unidades"))

    def validar_parametros(self, horas):
        self._validar_horas(horas, self.MAX_HORAS)

    def calcular_costo_base(self, horas):
        # Horas por tarifa, más el seguro que se cobra una sola vez
        return self.tarifa_hora * horas + self.COSTO_SEGURO

    def describir(self):
        return (f"Equipo {self.identificador} '{self.nombre}' ({self._equipo}), "
                f"{self._unidades} unidades, ${self.tarifa_hora:,.0f}/hora")


class Asesoria(Servicio):
    """Asesoría especializada."""
    MAX_HORAS = 8
    # Multiplicador de precio según la experiencia del asesor
    NIVELES = {"junior": 1.0, "senior": 1.3, "experto": 1.6}

    def __init__(self, identificador, nombre=None, tarifa_hora=None,
                 especialidad=None, nivel=None):
        super().__init__(identificador, nombre, tarifa_hora)
        if especialidad is None or not str(especialidad).strip():
            raise ParametroFaltanteError("Falta la especialidad")
        # Solo se aceptan los niveles definidos en NIVELES
        if nivel not in self.NIVELES:
            raise ParametroInvalidoError(
                f"Nivel inválido, use: {', '.join(self.NIVELES)}", detalle=nivel)
        self._especialidad = str(especialidad).strip()
        self._nivel = nivel

    def validar_parametros(self, horas):
        self._validar_horas(horas, self.MAX_HORAS)

    def calcular_costo_base(self, horas):
        # El precio sube según el nivel del asesor (junior, senior o experto)
        return self.tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        return (f"Asesoría {self.identificador} '{self.nombre}' de "
                f"{self._especialidad} (nivel {self._nivel}), "
                f"${self.tarifa_hora:,.0f}/hora")
