"""
main_miguel.py - Simulación de 20 operaciones (válidas e inválidas) de Software FJ.
Integrante responsable: Miguel Ángel Echeverría Caballero
Ejecución: python main_miguel.py

La idea es demostrar que el sistema no se cae cuando algo sale mal:
cada operación se ejecuta de forma aislada y los errores se registran.
"""
from excepciones_eva import SoftwareFJError
from gestor_Manuel_Ospino import GestorSoftwareFJ
from registro_eva import ARCHIVO_LOG, obtener_logger

logger = obtener_logger()


def cadena_de_causas(error):
    """Recorre las causas encadenadas (raise ... from ...) y las une en un texto."""
    causas = []
    actual = error.__cause__
    # Vamos "bajando" por la cadena hasta llegar a la causa original
    while actual is not None:
        causas.append(str(actual))
        actual = actual.__cause__
    return " <- ".join(causas)


def ejecutar_operacion(numero, descripcion, funcion):
    """
    Ejecuta una operación sin que un error detenga el programa.
    Usa try/except/else/finally. Devuelve True si fue exitosa.
    """
    print(f"\n[{numero:02d}] {descripcion}")
    logger.info("INICIO operación %02d: %s", numero, descripcion)
    exito = False
    try:
        resultado = funcion()
    except SoftwareFJError as error:                # Error controlado del sistema
        # Son los errores que nosotros mismos definimos y esperábamos
        causa = cadena_de_causas(error)
        print(f"     ✗ Error controlado: {error}")
        if causa:
            print(f"       causa: {causa}")
        logger.error("Operación %02d falló: %s | causa: %s", numero, error,
                     causa or "N/A")
    except Exception as error:                      # Error inesperado
        # Cualquier otra cosa que no previmos; se registra como crítico con traza
        print(f"     ✗ Error inesperado ({type(error).__name__}): {error}")
        logger.critical("Operación %02d error inesperado: %s: %s", numero,
                        type(error).__name__, error, exc_info=True)
    else:
        # Solo llega aquí si no hubo ninguna excepción
        print(f"     ✓ OK: {resultado}")
        logger.info("Operación %02d exitosa: %s", numero, resultado)
        exito = True
    finally:
        # Esto se ejecuta siempre, haya salido bien o mal
        logger.info("FIN operación %02d", numero)
    return exito


def confirmar_y_procesar(gestor, id_reserva, descuento=None):
    """Busca una reserva, la confirma y luego la procesa (con descuento opcional)."""
    reserva = gestor.buscar_reserva(id_reserva)
    reserva.confirmar()
    reserva.procesar(descuento=descuento)
    return reserva


def bloquear_y_reservar(gestor):
    """Bloquea un servicio y después intenta reservarlo (debe fallar)."""
    gestor.buscar_servicio("SRV-003").bloquear()
    return gestor.crear_reserva("CLI-001", "SRV-003", 2)


def main():
    g = GestorSoftwareFJ()
    # Cada operación es una pareja (descripción, función a ejecutar).
    # Se usan lambdas para que no se ejecuten hasta que ejecutar_operacion las llame.
    operaciones = [
        # ---- Clientes ----
        ("Registrar cliente válido (Ana)", lambda: g.registrar_cliente(
            nombre="ana pérez", documento="1045123456", correo="ana@mail.com",
            telefono="3001234567")),
        ("Registrar cliente válido (Luis)", lambda: g.registrar_cliente(
            nombre="Luis Gómez", documento="72345678", correo="luis@mail.com",
            telefono="3109876543")),
        ("Registrar cliente con correo inválido", lambda: g.registrar_cliente(
            nombre="Pedro Ruiz", documento="9988776", correo="pedro-correo",
            telefono="3205554433")),
        ("Registrar cliente sin nombre (parámetro faltante)", lambda: g.registrar_cliente(
            documento="5544332", correo="x@mail.com", telefono="3151112233")),
        ("Registrar cliente con documento duplicado", lambda: g.registrar_cliente(
            nombre="Ana Clon", documento="1045123456", correo="clon@mail.com",
            telefono="3001112222")),
        # ---- Servicios ----
        ("Crear sala válida", lambda: g.registrar_servicio(
            "sala", nombre="Sala Caribe", tarifa_hora=50000, capacidad=10)),
        ("Crear alquiler de equipo válido", lambda: g.registrar_servicio(
            "equipo", nombre="Portátil Pro", tarifa_hora=8000, equipo="Laptop",
            unidades=5)),
        ("Crear asesoría válida", lambda: g.registrar_servicio(
            "asesoria", nombre="Asesoría en Python", tarifa_hora=90000,
            especialidad="Programación", nivel="senior")),
        ("Crear servicio con tarifa negativa", lambda: g.registrar_servicio(
            "sala", nombre="Sala Fallida", tarifa_hora=-100, capacidad=8)),
        ("Crear servicio de tipo inexistente", lambda: g.registrar_servicio(
            "transporte", nombre="Taxi", tarifa_hora=1000)),
        # ---- Reservas ----
        ("Reserva exitosa: Ana en sala 3 h",
         lambda: g.crear_reserva("CLI-001", "SRV-001", 3)),
        ("Reserva exitosa: Luis alquila equipo 24 h",
         lambda: g.crear_reserva("CLI-002", "SRV-002", 24)),
        ("Reserva con duración excesiva (asesoría 20 h)",
         lambda: g.crear_reserva("CLI-001", "SRV-003", 20)),
        ("Reserva con cliente inexistente",
         lambda: g.crear_reserva("CLI-999", "SRV-001", 2)),
        ("Reserva sobre servicio bloqueado", lambda: bloquear_y_reservar(g)),
        # ---- Procesamiento ----
        ("Confirmar y procesar RES-001 con 10 % de descuento",
         lambda: confirmar_y_procesar(g, "RES-001", descuento=0.10)),
        ("Procesar RES-002 sin confirmar (operación no permitida)",
         lambda: g.buscar_reserva("RES-002").procesar()),
        ("Confirmar RES-002 y procesar con 90 % de descuento (cálculo inconsistente)",
         lambda: confirmar_y_procesar(g, "RES-002", descuento=0.90)),
        # cancelar() no devuelve nada, por eso el "or" para tener un mensaje que mostrar
        ("Cancelar RES-002",
         lambda: g.buscar_reserva("RES-002").cancelar() or "Reserva cancelada"),
        ("Fallo inesperado (división por cero)", lambda: 1 / 0),
    ]

    # Ejecutamos todas y contamos las exitosas (True cuenta como 1 al sumar)
    exitosas = sum(ejecutar_operacion(n, d, f)
                   for n, (d, f) in enumerate(operaciones, start=1))

    # Resumen final: el programa siguió funcionando pese a los errores
    print("\n" + "=" * 60)
    print(f"Operaciones: {len(operaciones)} | exitosas: {exitosas} | "
          f"con error controlado: {len(operaciones) - exitosas}")
    print("Estado final del sistema:")
    # Mostramos todo lo que quedó registrado: clientes, servicios y reservas
    for entidad in g.clientes + g.servicios + g.reservas:
        print("  ", entidad)
    print(f"\nRegistro completo en: {ARCHIVO_LOG}")
    logger.info("Simulación finalizada: %d operaciones, %d exitosas",
                len(operaciones), exitosas)


if __name__ == "__main__":
    main()
