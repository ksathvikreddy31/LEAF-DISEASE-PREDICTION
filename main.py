import streamlit as st
import numpy as np
from PIL import Image
import cv2
from keras.models import load_model

# Load the model
# model = load_model(r'C:\Users\jayan\OneDrive\Documents\Leaf-disease-detection\my_model.h5')
model = load_model(r'E:\projects\Leaf-disease-detection\my_model.h5')

# Function to preprocess the uploaded image
def preprocess_image(image):
    img_array = np.array(image)
    
    # Ensure image has 3 channels (RGB)
    if img_array.shape[-1] != 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    
    img_array = cv2.resize(img_array, (256, 256))  # Resize to 256x256
    img_array = img_array.astype('float32') / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    print("Image shape before prediction:", img_array.shape)
    
    return img_array

st.title("Leaf Disease Detection")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type="jpg")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    
    # Preprocess the uploaded image
    img_array = preprocess_image(image)

    # Make prediction
    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)

    # Map the predicted class to disease names
    classes = ['Corn-Common_rust', 'Potato-Early_blight', 'Tomato-Bacterial_spot']
    
    st.write(f"Predicted Disease: {classes[predicted_class]}")
