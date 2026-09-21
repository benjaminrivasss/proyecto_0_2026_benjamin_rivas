import funciones_analisis
import sys

if len(sys.argv) != 2:
    print("Uso: python analisis_smn.py datos/observaciones_smn.txt")
else:
    ruta = sys.argv[1]

    observaciones = leer_observaciones(ruta)

    mostrar_resumen(observaciones)