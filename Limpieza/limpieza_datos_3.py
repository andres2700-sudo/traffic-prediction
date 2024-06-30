import pandas as pd

# Cargar el archivo CSV
archivo_entrada = 'datos_id_3841_modificado.csv'
df = pd.read_csv(archivo_entrada)

# Convertir la columna 'fecha' al tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S').dt.time  


fechas_partidos = [
    "2022-01-08", "2022-01-23", "2022-02-06", "2022-02-19", "2022-03-05",
    "2022-03-09", "2022-03-20", "2022-04-09", "2022-04-12", "2022-04-30",
    "2022-05-04", "2022-05-12", "2022-05-20", "2022-07-24", "2022-07-27",
    "2022-07-31", "2022-08-10", "2022-09-03", "2022-09-11", "2022-09-14",
    "2022-10-02", "2022-10-05", "2022-10-16", "2022-10-22", "2022-10-30",
    "2022-11-02", "2022-11-10", "2023-01-11", "2023-01-15", "2023-01-26",
    "2023-01-29", "2023-02-02", "2023-02-11", "2023-02-15", "2023-02-25",
    "2023-03-02", "2023-03-11", "2023-03-15", "2023-04-02", "2023-04-08",
    "2023-04-12", "2023-04-22", "2023-04-29", "2023-05-06", "2023-05-09",
    "2023-05-13", "2023-05-24", "2023-06-04", "2023-07-24", "2023-07-27",
    "2023-09-02", "2023-09-17", "2023-09-20", "2023-09-27", "2023-10-07",
    "2023-11-05", "2023-11-08", "2023-11-11", "2023-11-29", "2023-12-02",
    "2023-12-17"
]


fechas_festivas = [
    "2022-01-01", "2022-01-06", "2022-04-14", "2022-04-15", "2022-05-02",
    "2022-05-16", "2022-07-25", "2022-08-15", "2022-10-12", "2022-11-01",
    "2022-11-09", "2022-12-06", "2022-12-08", "2022-12-26", "2023-01-06",
    "2023-03-20", "2023-04-06", "2023-04-07", "2023-05-01", "2023-05-15",
    "2023-08-15", "2023-10-12", "2023-11-01", "2023-11-09", "2023-12-06",
    "2023-12-08", "2023-12-25"
]


df['hubo_partido'] = df.apply(lambda x: x['fecha'].date().isoformat() in fechas_partidos and x['hora'] >= pd.to_datetime('16:00:00').time() and x['hora'] <= pd.to_datetime('22:00:00').time(), axis=1)


df['es_festivo'] = df['fecha'].dt.date.isin([pd.to_datetime(fecha).date() for fecha in fechas_festivas])


def determinar_periodo(hora):
    if 6 <= hora.hour < 12:
        return 'Mañana'
    elif 12 <= hora.hour < 18:
        return 'Tarde'
    elif 18 <= hora.hour < 22:
        return 'Noche'
    else:
        return 'Madrugada'


df['periodo_dia'] = df['hora'].apply(determinar_periodo)


archivo_salida = 'datos_id_3041_modificado_con_eventos.csv'
df.to_csv(archivo_salida, index=False)

print(f"Archivo '{archivo_salida}' creado con éxito.")
