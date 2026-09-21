# Trabajo Práctico - Observaciones Meteorológicas del SMN

## Descripción

Este programa fue realizado para el Trabajo Práctico de Programación 1.

Lee un archivo de observaciones actuales del Servicio Meteorológico Nacional (SMN), guarda la información en un diccionario y luego obtiene distintas estadísticas sobre las observaciones, como temperaturas máximas y mínimas, velocidad del viento, datos faltantes y rankings de ciudades.

---

## Cómo ejecutar el programa

Ubicarse en la carpeta del proyecto y ejecutar:

```bash
python analisis_smn.py datos/observaciones_smn.txt
```

---

## Cómo obtener el archivo de entrada

1. Ingresar a la página del Servicio Meteorológico Nacional:

   https://www.smn.gob.ar/descarga-de-datos

2. Descargar el archivo **Observaciones actuales**.

3. Descomprimir el archivo `.rar`.

4. Copiar el archivo `.txt` dentro de la carpeta `datos/` del proyecto.

---

## Funciones del programa

El programa permite:

- Leer el archivo de observaciones.
- Guardar la información en un diccionario.
- Separar la dirección y la velocidad del viento.
- Contar la cantidad de ciudades leídas.
- Contar las ciudades con todos los datos completos.
- Mostrar los datos faltantes por campo.
- Obtener la temperatura máxima y mínima.
- Obtener la velocidad máxima y mínima del viento.
- Mostrar el Top 5 de ciudades:
  - más cálidas.
  - más frías.
  - con mayor velocidad de viento.
  - con menor velocidad de viento.

---

## Ejemplo de salida

```text
RESUMEN

Cantidad de ciudades: 89
Cantidad de ciudades completas: 76

Temperatura máxima:
Formosa: 31.2

Temperatura mínima:
Ushuaia: -1.4

Datos faltantes:
- sensacion_termica: 5 dato(s)
  Ciudades: Benito Juárez, ...

Mayor velocidad de viento:
Comodoro Rivadavia: 42.0

Menor velocidad de viento:
Azul: 0.0

Top 5 ciudades más cálidas:
Formosa: 31.2
Resistencia: 30.8
Posadas: 29.9
Corrientes: 29.4
Reconquista: 28.7
```