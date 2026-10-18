import sys
from pathlib import Path

from funciones_smn import (
    leer_observaciones,
    guardar_json,
    leer_json,
    cantidad_ciudades,
    cantidad_ciudades_completas,
    contar_archivos
)


def main():
    """
    Programa principal para procesar archivos del SMN.
    """

    # Sin argumentos
    if len(sys.argv) == 1:
        print("No se proporcionó ningún archivo.")

        cantidad_txt = contar_archivos("datos", ".txt")
        cantidad_json = contar_archivos("obs_json", ".json")

        print(f"Archivos TXT disponibles: {cantidad_txt}")
        print(f"Archivos JSON disponibles: {cantidad_json}")
        return

    # Más de un argumento
    if len(sys.argv) > 2:
        print("Error: se proporcionó más de un argumento.")
        return

    ruta = sys.argv[1]
    archivo = Path(ruta)
    extension = archivo.suffix.lower()

    # Archivo TXT
    if extension == ".txt":

        if not archivo.is_file():
            print(f"Error: no se encontró el archivo '{ruta}'.")
            return

        if Path("datos").resolve() not in archivo.resolve().parents:
            print("Error: los archivos TXT deben estar dentro de datos/.")
            return

        print("Leyendo archivo TXT...")

        observaciones = leer_observaciones(ruta)

        if len(observaciones) == 0:
            print("No se encontraron observaciones válidas.")
            return

        try:
            guardar_json(observaciones, ruta)
        except OSError as error:
            print(f"Error al guardar el JSON: {error}")
            return

    # Archivo JSON
    elif extension == ".json":

        try:
            observaciones = leer_json(ruta)
        except (OSError, ValueError) as error:
            print(f"Error al leer el JSON: {error}")
            return

        if not isinstance(observaciones, dict):
            print("Error: el JSON no contiene un diccionario.")
            return

    # Extensión no válida
    else:
        print("Error: extensión no soportada.")
        return

    # Resultados
    print(f"Cantidad de ciudades: {cantidad_ciudades(observaciones)}")
    print(f"Cantidad de ciudades completas: {cantidad_ciudades_completas(observaciones)}")


if __name__ == "__main__":
    main()