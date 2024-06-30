import os

# Estructura de carpetas
folders = [
    'templates',
    'static/css',
    'static/js'
]

# Crear estructura de directorios
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Crear archivos básicos
with open('app.py', 'w') as f:
    f.write("""
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
""")

with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Predicción de Intensidad de Tráfico</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Predicción de Intensidad de Tráfico</h1>
    <form id="predictionForm">
        <label for="date">Fecha y hora:</label>
        <input type="datetime-local" id="date" name="date" required><br><br>
        <input type="submit" value="Predecir">
    </form>
    <div id="predictionResult"></div>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>
</html>
""")

with open('static/css/style.css', 'w') as f:
    f.write("""
body {
    font-family: Arial, sans-serif;
    margin: 40px;
}
""")

with open('static/js/script.js', 'w') as f:
    f.write("""
document.getElementById('predictionForm').onsubmit = function(event) {
    event.preventDefault();
    var formData = new FormData(document.getElementById('predictionForm'));
    fetch('/', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          document.getElementById('predictionResult').innerHTML = 'Predicción de intensidad: ' + data.prediction;
      })
      .catch(error => console.error('Error:', error));
};
""")

print("Proyecto Flask estructurado creado con éxito.")
