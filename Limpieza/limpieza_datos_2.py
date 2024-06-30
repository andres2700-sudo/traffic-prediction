import pandas as pd


archivo_entrada = 'datos_id_3840.csv'
df = pd.read_csv(archivo_entrada)

df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.month_name()
df['dia'] = df['fecha'].dt.day_name()
df['hora'] = df['fecha'].dt.strftime('%H:%M:%S')


df['es_fin_de_semana'] = df['fecha'].dt.dayofweek >= 5
df['fecha'] = df['fecha'].dt.date

df_final = df[['id', 'fecha', 'mes', 'dia', 'hora', 'intensidad', 'carga', 'es_fin_de_semana']]
archivo_salida = 'datos_id_3840_modificado.csv'
df_final.to_csv(archivo_salida, index=False)

print(f"Archivo '{archivo_salida}' creado con éxito.")
