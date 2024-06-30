from flask import Flask, request, render_template, session, redirect, url_for
import joblib
import numpy as np
import subprocess
import logging
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import pandas as pd


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'una_clave_secreta' 

# Carga el modelo de predicción
model = joblib.load('traffic_model.pkl')

# escenarios de carga
scenarios = {
    'low': 0.10,    
    'medium': 0.45,  
    'high': 1.00      
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'predict':
            
            scenario = request.form['scenario']
            carga = scenarios[scenario]
            es_fin_de_semana = int(request.form.get('es_fin_de_semana', 0))
            hubo_partido = int(request.form.get('hubo_partido', 0))
            es_festivo = int(request.form.get('es_festivo', 0))
            mes = request.form['mes']
            dia = request.form['dia']
            hora = int(request.form['hora'])

            # convertir a coordenadas ciclicas
            mes_sin, mes_cos = get_cyclic_coordinates(mes, 'mes')
            dia_sin, dia_cos = get_cyclic_coordinates(dia, 'dia')
            hora_sin = np.sin(hora * (2 * np.pi / 24))
            hora_cos = np.cos(hora * (2 * np.pi / 24))

            input_data = [carga, es_fin_de_semana, hubo_partido, es_festivo, mes_sin, mes_cos, dia_sin, dia_cos, hora_sin, hora_cos]
            input_df = pd.DataFrame([input_data], columns=['carga', 'es_fin_de_semana', 'hubo_partido', 'es_festivo', 'mes_sin', 'mes_cos', 'dia_sin', 'dia_cos', 'hora_sin', 'hora_cos'])
            predicted_intensity = model.predict(input_df)[0] * 1000
            session['predicted_intensity'] = predicted_intensity

            logging.debug(f"Predicted intensity: {predicted_intensity}")

            return render_template('index.html', prediction=f"La intensidad del tráfico predicha es: {predicted_intensity} veh/hora")

        elif action == 'simulate':
            predicted_intensity = session.get('predicted_intensity', None)
            if predicted_intensity:
                interval = 3600 / predicted_intensity
                commands = [
                    f"python $SUMO_HOME/tools/randomTrips.py -n red.sumo.xml -e 3600 -p {interval:.2f} -o demanda.trips.xml",
                    f"$SUMO_HOME/bin/duarouter --route-files demanda.trips.xml --net-file red.sumo.xml --output-file rutas.rou.xml --ignore-errors true",
                    "$SUMO_HOME/bin/sumo-gui archivo.sumocfg"  
                ]
                for cmd in commands:
                    run_command(cmd)
                
                
                simulation_summary = parse_summary_file('summary.xml')
                create_traffic_plot(simulation_summary) 

                
                filtered_summary = simulation_summary[simulation_summary['time'] == '3599.00']

                return render_template('index.html', simulation_summary=filtered_summary.to_dict('records'), prediction=f"La intensidad del tráfico predicha es: {predicted_intensity} veh/hora")
            else:
                return render_template('index.html', error="Primero debe predecir la intensidad del tráfico antes de simular.")

    return render_template('index.html', prediction=None)

@app.route('/reset', methods=['GET'])
def reset():
    session.clear()
    return redirect(url_for('index'))

def get_cyclic_coordinates(value, type):
    meses = {
        "January": (0.5, 0.866), "February": (0.866, 0.5), "March": (1.0, 0),
        "April": (0.866, -0.5), "May": (0.5, -0.866), "June": (0, -1.0),
        "July": (-0.5, -0.866), "August": (-0.866, -0.5), "September": (-1.0, 0),
        "October": (-0.866, 0.5), "November": (-0.5, 0.866), "December": (0, 1.0)
    }
    dias = {
        "Monday": (0.0, 1.0), "Tuesday": (0.782, 0.623), "Wednesday": (0.975, -0.223),
        "Thursday": (0.434, -0.901), "Friday": (-0.434, -0.901), "Saturday": (-0.975, -0.223),
        "Sunday": (-0.782, 0.623)
    }
    if type == 'mes':
        return meses.get(value, (0, 0))
    elif type == 'dia':
        return dias.get(value, (0, 0))

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    filtered_output = "\n".join(line for line in output.decode('utf-8').split("\n") if not line.startswith("Warning"))
    filtered_error = "\n".join(line for line in error.decode('utf-8').split("\n") if not line.startswith("Warning"))
    with open("simulation_output.log", "a") as log_file:
        log_file.write(f"Comando: {command}\n")
        log_file.write(f"Salida: {filtered_output}\n")
        log_file.write(f"Error: {filtered_error}\n")
    return {'command': command, 'output': filtered_output, 'error': filtered_error}

def parse_summary_file(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    data = []
    for timestep in root.findall('step'):
        step_data = {}
        for attr in timestep.attrib:
            step_data[attr] = timestep.attrib[attr]
        data.append(step_data)
    
    df = pd.DataFrame(data)
    return df

def create_traffic_plot(df):
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'].astype(float), df['running'].astype(float), label='Vehículos en Movimiento', color='blue', marker='o')
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Vehículos en Movimiento [#]')
    plt.title('Vehículos en Movimiento a lo Largo del Tiempo')
    plt.grid(True)
    plt.legend()
    plt.savefig('static/traffic_plot.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
