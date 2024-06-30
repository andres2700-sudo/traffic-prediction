import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from math import sin, cos, pi
import matplotlib.pyplot as plt


df = pd.read_csv('dataset.csv')


df['fecha'] = pd.to_datetime(df['fecha'])
df['mes'] = df['fecha'].dt.month
df['dia'] = df['fecha'].dt.dayofweek


df['hora'] = pd.to_datetime(df['hora'], format='%H:%M:%S')
df['hora_decimal'] = df['hora'].dt.hour
df['minuto_decimal'] = df['hora'].dt.minute


def convertir_ciclico(valor, max_val):
    sin_val = sin(2 * pi * valor / max_val)
    cos_val = cos(2 * pi * valor / max_val)
    return sin_val, cos_val

# transformaciones cíclicas
df['mes_sin'], df['mes_cos'] = zip(*df['mes'].apply(lambda x: convertir_ciclico(x, 12)))
df['dia_sin'], df['dia_cos'] = zip(*df['dia'].apply(lambda x: convertir_ciclico(x, 7)))
df['hora_sin'], df['hora_cos'] = zip(*df['hora_decimal'].apply(lambda x: convertir_ciclico(x, 24)))
df['minuto_sin'], df['minuto_cos'] = zip(*df['minuto_decimal'].apply(lambda x: convertir_ciclico(x, 60)))


df['es_fin_de_semana'] = df['es_fin_de_semana'].astype(int)
df['hubo_partido'] = df['hubo_partido'].astype(int)
df['es_festivo'] = df['es_festivo'].astype(int)
periodo_a_numero = {'Madrugada': 1, 'Mañana': 2, 'Tarde': 3, 'Noche': 4}
df['periodo_dia'] = df['periodo_dia'].map(periodo_a_numero)

#scaler = MinMaxScaler()
#df[['intensidad', 'carga']] = scaler.fit_transform(df[['intensidad', 'carga']])
# Escalado
df['carga'] = df['carga'] / 10.0





# Visualización de distribuciones cíclicas
plt.figure(figsize=(12, 12))
plt.subplot(4, 1, 1)
plt.scatter(df['mes_sin'], df['mes_cos'], alpha=0.5)
plt.title('Distribución Cíclica de Meses')
plt.subplot(4, 1, 2)
plt.scatter(df['dia_sin'], df['dia_cos'], alpha=0.5)
plt.title('Distribución Cíclica de Días de la Semana')
plt.subplot(4, 1, 3)
plt.scatter(df['hora_sin'], df['hora_cos'], alpha=0.5)
plt.title('Distribución Cíclica de Horas')
plt.subplot(4, 1, 4)
plt.scatter(df['minuto_sin'], df['minuto_cos'], alpha=0.5)
plt.title('Distribución Cíclica de Minutos')

plt.tight_layout()
plt.show()

# Eliminar columnas innecesarias 
df.drop(['fecha', 'mes', 'dia', 'hora', 'hora_decimal', 'minuto_decimal'], axis=1, inplace=True)
df.to_csv('dataset_final.csv', index=False)
print("Dataset preparado y guardado con éxito.")
