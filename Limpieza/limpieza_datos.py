import pandas as pd
import os
from tqdm import tqdm  


carpeta_datos = './datos_madrid_2023/datos_trafico'  


id_interes = 3840


dfs = []


archivos_csv = [archivo for archivo in os.listdir(carpeta_datos) if archivo.endswith('.csv')]


for archivo in tqdm(archivos_csv, desc="Procesando archivos CSV"):
    ruta_completa = os.path.join(carpeta_datos, archivo)
    
    try:
        df_temp = pd.read_csv(ruta_completa, delimiter=';', usecols=['id', 'fecha', 'intensidad', 'carga'])
       
        df_temp = df_temp[df_temp['id'] == id_interes]
        dfs.append(df_temp)
    except Exception as e:
        print(f"Error al procesar {archivo}: {e}")


df_filtrado_total = pd.concat(dfs, ignore_index=True)


df_filtrado_total['fecha'] = pd.to_datetime(df_filtrado_total['fecha'], format='%Y-%m-%d %H:%M:%S')


df_filtrado_total = df_filtrado_total[(df_filtrado_total['intensidad'] >= 0) & (df_filtrado_total['carga'] >= 0)]


nombre_archivo_salida = 'datos_id_3840.csv'  
df_filtrado_total.to_csv(nombre_archivo_salida, index=False)

print(f"Datos filtrados guardados en {nombre_archivo_salida}")
