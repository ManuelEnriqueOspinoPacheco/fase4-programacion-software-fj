# Software FJ

Este Proyecto de la Fase 4  del curso de Programación (213023), UNAD. Sistema orientado a objetos en Python

Este proyecto fue desarrollado por 3 estudiantes:

EVA MARIA BOLANO MANJARRES

MIGUEL ANGEL ECHEVERRIA CABALLERO

MANUEL ENRIQUE OSPINO PACHECO

## ¿Como se desarrollo?

Este proyecto fue dividido en los 3 estudiantes de forma ordenada, cada estudiante agrego su codigo por RAMA, Los estudiantes lo pudieron agregar subiendo el archivo o escribiendolo en GITHUB.

## ¿Que hace nuesto sistema?

Gestiona clientes, servicios (salas, equipos y asesoruas) y reservas de la empresa Software FJ.

## Requisitos para correr el Software 

- Python 3.10

## ¿Como ejecutarlo puedo ejecutarlo?

```bash
python main_miguel.py
```

## ¿Donde esta cada tecnica de manejo de errores?

- `try/except` con encadenamiento (`raise ... from ...`): `Reserva.__init__`, `GestorSoftwareFJ.registrar_cliente`, `Servicio.calcular_costo`
- `try/except/else`: `GestorSoftwareFJ.registrar_cliente` y `registrar_servicio`
- `try/finally`: `Reserva.confirmar`
- `try/except/else/finally`: `Reserva.procesar` y `ejecutar_operacion` en `main_miguel.py`

## Metodos sobrecargados

`Servicio.calcular_costo(horas, impuesto=None, descuento=None)` tiene tres variantes de llamada (solo horas, con impuesto, con impuesto y descuento) mediante parametros opcionales, ya que Python no tiene sobrecarga nativa.
