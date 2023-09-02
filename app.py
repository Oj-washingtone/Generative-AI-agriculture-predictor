from flask import Flask, render_template, request, redirect, url_for
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
import numpy as np

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load a pre-trained CNN model (VGG16 in this example)
model = VGG16(weights='imagenet')

# Function to check if the file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process the uploaded image and get suggestions
def analyze_soil_image(file):
    img = image.load_img(file, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    
    # Get the CNN predictions for the image
    predictions = model.predict(x)
    decoded_predictions = decode_predictions(predictions, top=3)[0]
    
    # Generate suggestions based on the predictions (replace with your generative AI code)
    suggestions = [f"{label}: {score:.2f}" for _, label, score in decoded_predictions]
    
    return suggestions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Analyze the uploaded image and get suggestions
        suggestions = analyze_soil_image(filename)

        # Display the suggestions on a new page or return them as JSON
        return render_template('suggestions.html', suggestions=suggestions)

    return "Invalid file format"

if __name__ == '__main__':
    app.run(debug=True)