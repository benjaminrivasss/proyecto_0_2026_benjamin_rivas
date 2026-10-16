import sys
from pathlib import Path

from funciones_smn import (
    leer_observaciones,
    guardar_json,
    leer_json,
    cantidad_ciudades,
    cantidad_ciudades_completas
)


def main():
    """
    Ejecuta el programa principal.
    """

    if len(sys.argv) != 2:
        print("Uso: python3 analisis_smn.py datos/observaciones_smn.txt")
        return

    ruta = sys.argv[1]

    extension = Path(ruta).suffix.lower()

    print(f"Extensión detectada: {extension}")

    if extension == ".txt":
        print("Archivo del SMN, convirtiendo a JSON...")

        observaciones = leer_observaciones(ruta)

        if len(observaciones) == 0:
            return

        guardar_json(observaciones, ruta)

    elif extension == ".json":
        print("Archivo JSON detectado.")

        observaciones = leer_json(ruta)

    else:
        print("Error: extensión no soportada.")
        return

    print(f"Cantidad de ciudades: {cantidad_ciudades(observaciones)}")
    print(f"Cantidad de ciudades completas: {cantidad_ciudades_completas(observaciones)}")


if __name__ == "__main__":
    main()