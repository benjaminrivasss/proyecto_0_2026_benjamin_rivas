from funciones_analisis import leer_observaciones, mostrar_resumen


def main():
    """
    Ejecuta el programa principal.
    """

    ruta = input("Ingrese la ruta del archivo: ")

    observaciones = leer_observaciones(ruta)

    mostrar_resumen(observaciones)


main()