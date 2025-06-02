from flask import Flask, request, jsonify, render_template_string, send_from_directory
from PIL import Image
import random
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class_names = ['Apple Scab', 'Black Rot', 'Cedar Apple Rust', 'Leaf Blight','Black rot','Mosaic virus','Leaf spot wilt']

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Crop Disease Predictor</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #a8edea, #fed6e3);
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .container {
      background: #fff;
      padding: 40px;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
      width: 100%;
      max-width: 500px;
      text-align: center;
    }
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
    input[type="file"] {
      margin: 15px 0;
    }
    button {
      background: #00c853;
      color: white;
      padding: 12px 30px;
      border: none;
      border-radius: 25px;
      font-size: 1em;
      cursor: pointer;
    }
    button:hover {
      background: #00b44b;
    }
    #result {
      margin-top: 20px;
      font-size: 1.2em;
      color: #444;
      font-weight: bold;
    }
    #preview {
      margin-top: 15px;
      max-width: 100%;
      border-radius: 12px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🌿 Crop Disease Predictor</h1>
    <form id="uploadForm" enctype="multipart/form-data">
      <input type="file" name="image" id="imageInput" accept="image/*" required><br>
      <button type="submit">Predict Disease</button>
    </form>
    <img id="preview" src="" style="display:none;">
    <div id="result"></div>
  </div>

  <script>
    const form = document.getElementById('uploadForm');
    const preview = document.getElementById('preview');
    const imageInput = document.getElementById('imageInput');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(form);

      const response = await fetch('/predict', {
        method: 'POST',
        body: formData
      });

      const result = await response.json();

      if (result.image_url) {
        preview.src = result.image_url;
        preview.style.display = 'block';
      }

      resultDiv.innerText = "🌱 Prediction: " + result.prediction;
    });

    imageInput.addEventListener('change', () => {
      const file = imageInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => {
          preview.src = e.target.result;
          preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        img = Image.open(file).convert("RGB")
        img.verify()

        # Save image
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.seek(0)
        file.save(file_path)

        # Random prediction
        prediction = random.choice(class_names)

        return jsonify({
            'prediction': prediction,
            'image_url': f'/static/uploads/{filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
