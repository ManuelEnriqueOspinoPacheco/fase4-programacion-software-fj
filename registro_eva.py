import logging
import os

# Ruta de la carpeta donde se almacenarán los registros.
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

# Nombre y ruta del archivo donde se guardarán los eventos y errores.
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def obtener_logger():
    """
    Configura y devuelve el logger de Software FJ.
    Evita crear manejadores duplicados y conserva los registros anteriores.
    """
    logger = logging.getLogger("software_fj")

    # Verifica si el logger ya fue configurado.
    if logger.handlers:
        return logger

    try:
        # Crea la carpeta logs si todavía no existe.
        os.makedirs(RUTA_LOGS, exist_ok=True)

        # Configura el nivel de registro.
        logger.setLevel(logging.DEBUG)

        # Crea el manejador para escribir en el archivo de log.
        manejador = logging.FileHandler(
            ARCHIVO_LOG,
            mode="a",
            encoding="utf-8"
        )

        # Define el formato de los registros.
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"
        )
        manejador.setFormatter(formato)

        # Agrega el manejador al logger.
        logger.addHandler(manejador)

        # Evita que los mensajes se repitan en otros loggers.
        logger.propagate = False

        logger.info("Sistema de registro de Software FJ configurado correctamente.")

    except OSError:
        # Si no es posible crear o abrir el archivo de log,
        # se informa el problema y se propaga la excepción.
        raise

    return logger
