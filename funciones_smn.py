from datetime import datetime
MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def convertir_fecha_y_hora(fecha: str, hora: str) -> datetime:
    """
    Convierte una fecha del formato '10-septiembre-2026'
    y una hora del formato '14:00'
    en un único objeto datetime.
    """
    dia, mes, anio = fecha.split("-")
    horas, minutos = hora.split(":")

    return datetime(
        int(anio),
        MESES[mes.lower()],
        int(dia),
        int(horas),
        int(minutos)
    )

def separar_viento(campo_viento: str) -> tuple:
    """
    Interpreta el campo de viento 'Norte 3' como (dirección, velocidad)
    y maneja el caso especial 'Calma'.
    """

    texto_limpio = campo_viento.strip()

    if texto_limpio.lower() == "calma":
        return ("Calma", 0.0)

    partes = texto_limpio.split()

    direccion = " ".join(partes[:-1])
    velocidad = float(partes[-1])

    return (direccion, velocidad)

def datos_faltantes(observaciones: dict) -> dict:
    """
    Devuelve un diccionario con la cantidad de datos faltantes
    por campo y las ciudades donde ocurren.
    """

    faltantes = {}

    for ciudad, datos in observaciones.items():

        for campo, valor in datos.items():

            if valor is None:

                if campo not in faltantes:
                    faltantes[campo] = {
                        "cantidad": 0,
                        "ciudades": []
                    }

                faltantes[campo]["cantidad"] += 1
                faltantes[campo]["ciudades"].append(ciudad)

    return faltantes

def leer_observaciones(ruta: str) -> dict:
    """
    Lee el archivo de observaciones del SMN y devuelve un diccionario:
    {ciudad: datos_diccionario}
    Maneja líneas mal formadas sin cortar la lectura.
    """
    observaciones = {}
    lineas_invalidas = 0

    try:
        archivo = open(ruta, "r", encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta '{ruta}'")
        return observaciones
    except Exception as error:
        print(f"Error al intentar abrir el archivo: {error}")
        return observaciones

    for linea in archivo:
        linea = linea.strip()

        if not linea:
            continue

        campos = linea.split(";")

        if len(campos) != 10:
            lineas_invalidas += 1
            continue

        ciudad = campos[0].strip()
        fecha_y_hora = convertir_fecha_y_hora(
            campos[1].strip(),
            campos[2].strip())
        condicion = campos[3].strip()
        visibilidad = campos[4].strip()

        try:
            temperatura = float(campos[5].strip())
        except ValueError:
            temperatura = None

        st_texto = campos[6].strip()
        if st_texto == "No se calcula" or st_texto == "":
            sensacion_termica = None
        else:
            try:
                sensacion_termica = float(st_texto)
            except ValueError:
                sensacion_termica = None

        try:
            humedad = float(campos[7].strip())
        except ValueError:
            humedad = None

        direccion_viento, velocidad_viento = separar_viento(campos[8])
        try:
            presion = float(campos[9].strip().split()[0].replace(",", "."))
        except ValueError:
            presion = None

        observaciones[ciudad] = {
            "fecha_y_hora": fecha_y_hora,
            "condicion": condicion,
            "visibilidad": visibilidad,
            "temperatura": temperatura,
            "sensacion_termica": sensacion_termica,
            "humedad": humedad,
            "direccion_viento": direccion_viento,
            "velocidad_viento": velocidad_viento,
            "presion": presion,
        }

    archivo.close()

    if lineas_invalidas > 0:
        print(f"[Aviso] Se ignoraron {lineas_invalidas} línea(s) con formato inválido.")

    return observaciones

def horarios_reportados(observaciones: dict) -> list:
    """
    Devuelve una lista de los horarios a los que las estaciones
    reportaron, en formato "HH:MM", sin repetir y ordenados
    de menor a mayor.
    """
    horarios = []

    for datos in observaciones.values():
        fecha_y_hora = datos["fecha_y_hora"]
        horario = fecha_y_hora.strftime("%H:%M")

        if horario not in horarios:
            horarios.append(horario)

    horarios.sort()

    return horarios

def cantidad_ciudades(observaciones: dict) -> int:
    """Devuelve la cantidad total de ciudades leídas."""
    return len(observaciones)

def cantidad_ciudades_completas(observaciones: dict) -> int:
    """Devuelve la cantidad de ciudades sin ningún dato faltante (None)."""
    completas = 0
    for ciudad, datos in observaciones.items():
        tiene_faltantes = False
        for valor in datos.values():
            if valor is None:
                tiene_faltantes = True
                break
        if not tiene_faltantes:
            completas += 1
    return completas

def top_n_ciudades(observaciones: dict, campo: str, n: int,descendente: bool = True) -> list:
    """
    Devuelve las n ciudades ordenadas según 'campo', de mayor a menor
    (o de menor a mayor si descendente=False) en una lista de tuplas (ciudad, valor).
    Descarta las estaciones donde el campo es None.
    """
    lista_validos = []

    for ciudad, datos in observaciones.items():
        valor = datos.get(campo)
        if valor is not None:
            lista_validos.append((ciudad, valor))

    # Función auxiliar interna para ordenar por el valor (segunda posición de la tupla)
    def obtener_valor(item):
        return item[1]

    lista_validos.sort(key=obtener_valor, reverse=descendente)
    return lista_validos[:n]

def mostrar_ranking(observaciones: dict,titulo: str,campo: str,n: int,descendente: bool = True,) -> None:
    """
    Muestra por pantalla las n ciudades ordenadas según el campo
    indicado, de mayor a menor o de menor a mayor.
    """

    print(f"\n{titulo}")

    ranking = top_n_ciudades(observaciones, campo, n, descendente)

    for ciudad, valor in ranking:
        print(f"{ciudad}: {valor}")
    print()
    
def mostrar_resumen(observaciones: dict) -> None:
    """
    Muestra por pantalla un resumen de las observaciones.
    """

    print("RESUMEN\n")

    print(f"Cantidad de ciudades: {cantidad_ciudades(observaciones)}")
    print(f"Cantidad de ciudades completas: {cantidad_ciudades_completas(observaciones)}")
    print(f"Horarios reportados: {', '.join(horarios_reportados(observaciones))}")

    mostrar_ranking(observaciones, "Temperatura máxima:", "temperatura", 1)

    mostrar_ranking(observaciones, "Temperatura mínima:", "temperatura", 1, False)

    faltantes = datos_faltantes(observaciones)

    print("\nDatos faltantes:")

    if not faltantes:
        print("No hay datos faltantes.")
    else:
        for campo, informacion in faltantes.items():

            print(f"- {campo}: {informacion['cantidad']} dato(s)")

            print("  Ciudades:")

            for ciudad in informacion["ciudades"]:
                print(f"   - {ciudad}")

            print()
    mostrar_ranking(observaciones, "Mayor velocidad de viento:", "velocidad_viento", 1)

    mostrar_ranking(observaciones, "Menor velocidad de viento:", "velocidad_viento", 1, False)

    mostrar_ranking(observaciones, "Top 5 ciudades más cálidas:", "temperatura", 5)

    mostrar_ranking(observaciones, "Top 5 ciudades más frías:", "temperatura", 5, False)

    mostrar_ranking(observaciones, "Top 5 ciudades con más viento:", "velocidad_viento", 5)

    mostrar_ranking(observaciones, "Top 5 ciudades con menos viento:", "velocidad_viento", 5, False)