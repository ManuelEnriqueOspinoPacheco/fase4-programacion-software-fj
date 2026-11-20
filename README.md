# Software FJ

Proyecto de la Fase 4 del curso Programación (213023), UNAD. Sistema orientado a objetos en Python

## Qué hace este sistema

Gestiona clientes, servicios (salas, equipos y asesorías) y reservas de la empresa Software FJ.

## Requisitos

- Python 3.10


## Dónde está cada técnica de manejo de errores

- `try/except` con encadenamiento (`raise ... from ...`): `Reserva.__init__`, `GestorSoftwareFJ.registrar_cliente`, `Servicio.calcular_costo`
- `try/except/else`: `GestorSoftwareFJ.registrar_cliente` y `registrar_servicio`
- `try/finally`: `Reserva.confirmar`
- `try/except/else/finally`: `Reserva.procesar` y `ejecutar_operacion` en `main_miguel.py`

## Métodos sobrecargados

`Servicio.calcular_costo(horas, impuesto=None, descuento=None)` tiene tres variantes de llamada (solo horas, con impuesto, con impuesto y descuento) mediante parámetros opcionales, ya que Python no tiene sobrecarga nativa.
