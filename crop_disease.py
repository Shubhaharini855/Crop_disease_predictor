import os
import random
from flask import Flask, request, jsonify, render_template_string
from PIL import Image

class_names = ['Apple Scab', 'Black Rot', 'Cedar Apple Rust', 'Leaf Blight','Anthrancose','Mosaic Virus','Spotted wilt virus']

app = Flask(__name__)

# Web HTML with CSS & JS
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Plant Disease Predictor</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #eef2f7;
      text-align: center;
      padding-top: 50px;
    }
    .container {
      background: white;
      padding: 30px;
      border-radius: 12px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
      width: 400px;
      margin: auto;
    }
    input[type="file"] {
      margin: 20px 0;
    }
    button {
      background-color: #28a745;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    #result {
      margin-top: 20px;
      font-size: 1.2em;
      color: #333;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Plant Disease Prediction</h1>
    <form id="uploadForm" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <br>
      <button type="submit">Predict</button>
    </form>
    <div id="result"></div>
  </div>

  <script>
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);

      const response = await fetch('/predict', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      document.getElementById('result').innerText = "Prediction: " + result.prediction;
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_template)

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Load and verify image
        img = Image.open(file).convert("RGB")
        img.verify()  # Just check it's a valid image

        # Return a random prediction
        predicted_class = random.choice(class_names)
        return jsonify({"prediction": predicted_class})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
