def separar_viento(campo_viento: str) -> tuple:
        """
    Interpreta el campo de viento 'Norte 3' como (dirección, velocidad) y maneja el caso especial 'Calma', sin velocidad numérica.
    """
        texto_limpio = campo_viento.strip()
        if texto_limpio.lower() == "calma":
            return ("Calma", 0.0)
    
        partes = texto_limpio.split()
    
        if len(partes) < 2:
            return (texto_limpio, 0.0)
    
        direccion = " ".join(partes[:-1])
        velocidad = float(partes[-1])
        return (direccion, velocidad)

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

        fecha = campos[1].strip()
        hora = campos[2].strip()
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
            presion = float(campos[9].strip())
        except ValueError:
            presion = None

        observaciones[ciudad] = {
            "fecha": fecha,
            "hora": hora,
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

def top_n_ciudades(
    observaciones: dict, campo: str, n: int, descendente: bool = True
) -> list:
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

def mostrar_resumen(observaciones: dict) -> None:
    """
    Muestra por pantalla un resumen de las observaciones.
    """

    print(" RESUMEN ")

    print(f"Cantidad de ciudades: {cantidad_ciudades(observaciones)}")
    print(f"Cantidad de ciudades completas: {cantidad_ciudades_completas(observaciones)}")

    print()

    print("Temperatura máxima:")
    print(top_n_ciudades(observaciones, "temperatura", 1))

    print()

    print("Temperatura mínima:")
    print(top_n_ciudades(observaciones, "temperatura", 1, False))

    print()

    print("Mayor velocidad de viento:")
    print(top_n_ciudades(observaciones, "velocidad_viento", 1))

    print()

    print("Menor velocidad de viento:")
    print(top_n_ciudades(observaciones, "velocidad_viento", 1, False))

    print()

    print("Top 5 ciudades más cálidas:")
    print(top_n_ciudades(observaciones, "temperatura", 5))

    print()

    print("Top 5 ciudades más frías:")
    print(top_n_ciudades(observaciones, "temperatura", 5, False))

    print()

    print("Top 5 ciudades con más viento:")
    print(top_n_ciudades(observaciones, "velocidad_viento", 5))

    print()

    print("Top 5 ciudades con menos viento:")
    print(top_n_ciudades(observaciones, "velocidad_viento", 5, False))