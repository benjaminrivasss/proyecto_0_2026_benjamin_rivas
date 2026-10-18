import sys
from pathlib import Path

from funciones_smn import (
    leer_observaciones,
    mostrar_resumen
)

from smn import main as main_smn


def main():
    """
    Ejecuta el análisis meteorológico original
    y las funcionalidades de la nueva consigna.
    """

    main_smn()

    if len(sys.argv) != 2:
        return

    ruta = sys.argv[1]

    if Path(ruta).suffix.lower() != ".txt":
        return

    observaciones = leer_observaciones(ruta)

    if len(observaciones) == 0:
        return

    mostrar_resumen(observaciones)


if __name__ == "__main__":
    main()