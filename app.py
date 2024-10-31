from flask import Flask, request, jsonify
from keras.preprocessing import image
import numpy as np
import os
from keras.models import load_model

app = Flask(__name__)

# Load your pre-trained model (replace 'your_model.h5' with your actual model path)
model = load_model('your_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Load and preprocess the image
    try:
        img = image.load_img(file_path, target_size=(224, 224))  # Adjust the size as needed
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0  # Normalize the image if your model requires it

        # Perform prediction using your model
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions)  # Get the index of the predicted class

        # Map the predicted class index to a class label (modify based on your model)
        class_labels = ['Healthy', 'Disease1', 'Disease2']  # Update with your actual class labels
        predicted_label = class_labels[predicted_class]

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Clean up: Remove the saved file after processing
    os.remove(file_path)

    return jsonify({'prediction': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
