
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
