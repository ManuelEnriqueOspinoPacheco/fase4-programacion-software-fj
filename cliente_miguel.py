"""
cliente_miguel.py - Clase Cliente con validaciones y encapsulación de datos personales.
Integrante responsable: Miguel Ángel Echeverría Caballero

Los datos personales del cliente son privados (con doble guion bajo) y solo
se pueden cambiar a través de los setters, que revisan que todo sea válido.
"""
import re

from entidad_miguel import Entidad
from excepciones_eva import ClienteInvalidoError, ParametroFaltanteError

# Formato básico de correo: texto + @ + dominio + al menos un punto (ej. ana@mail.com)
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales son atributos privados."""

    def __init__(self, identificador, nombre=None, documento=None,
                 correo=None, telefono=None):
        super().__init__(identificador)
        # Usamos los setters (self.nombre = ...) y no asignamos directo a los
        # atributos privados, para que cada dato pase por su validación
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @staticmethod
    def _requerido(valor, campo):
        """Revisa que el dato exista y no esté vacío; si falla, avisa cuál falta."""
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError(f"Falta el dato obligatorio '{campo}'")
        # Devolvemos el valor ya sin espacios sobrantes a los lados
        return str(valor).strip()

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = self._requerido(valor, "nombre")
        # Solo letras y espacios, mínimo 3 caracteres
        # (quitamos los espacios antes de usar isalpha, porque "Ana Pérez" tiene uno)
        if len(valor) < 3 or not valor.replace(" ", "").isalpha():
            raise ClienteInvalidoError("Nombre inválido", detalle=valor)
        # title() deja cada palabra con mayúscula inicial: "ana pérez" -> "Ana Pérez"
        self.__nombre = valor.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = self._requerido(valor, "documento")
        # Solo dígitos, entre 6 y 10 caracteres
        if not (valor.isdigit() and 6 <= len(valor) <= 10):
            raise ClienteInvalidoError("Documento inválido", detalle=valor)
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        valor = self._requerido(valor, "correo")
        # Comparamos contra el patrón de correo definido arriba
        if not PATRON_CORREO.match(valor):
            raise ClienteInvalidoError("Correo electrónico inválido", detalle=valor)
        # Guardamos en minúsculas para evitar duplicados por mayúsculas
        self.__correo = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = self._requerido(valor, "teléfono")
        # Celular colombiano: 10 dígitos
        if not (valor.isdigit() and len(valor) == 10):
            raise ClienteInvalidoError("Teléfono inválido", detalle=valor)
        self.__telefono = valor

    def describir(self):
        # Resumen corto del cliente; es lo que se ve al imprimirlo
        return (f"Cliente {self.identificador}: {self.nombre} "
                f"(doc. {self.documento}, {self.correo})")
