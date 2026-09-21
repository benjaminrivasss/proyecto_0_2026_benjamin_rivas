import sys

from funciones_analisis import leer_observaciones, mostrar_resumen


def main():
    """
    Ejecuta el programa principal.
    """

    if len(sys.argv) != 2:
        print("Uso: python analisis_smn.py datos/observaciones_smn.txt")
        return

    ruta = sys.argv[1]

    observaciones = leer_observaciones(ruta)

    if len(observaciones) == 0:
        return

    mostrar_resumen(observaciones)


main()