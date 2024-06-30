import pandas as pd


archivo1 = 'datos_id_3040_modificado_con_eventos.csv'
archivo2 = 'datos_id_3041_modificado_con_eventos.csv'


df1 = pd.read_csv(archivo1)
df2 = pd.read_csv(archivo2)


df_union = pd.concat([df1, df2], ignore_index=True)


df_union.drop('id', axis=1, inplace=True)

archivo_salida = 'dataset.csv'
df_union.to_csv(archivo_salida, index=False)

print(f"Archivo '{archivo_salida}' creado con éxito.")
