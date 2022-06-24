import tensorflow as tf
import cv2
from PIL import Image, ImageOps
import numpy as np

model = tf.keras.models.load_model('https://drive.google.com/file/d/1ua1D02e53COo8RPSCqGMUxQG3cFLq91C/view?usp=sharing')

import streamlit as st
st.write("""
         # Chest Opacity Classification
         """
         )
st.write("This is a simple image classification web app to diagnose chest opacities in patients")
file = st.file_uploader("Please upload an image file", type=["jpg", "png", "jpeg"])

def import_and_predict(image_data, model):
    
        
        img = cv2.resize(np.float32(image_data),(96,122))
        image = img.reshape([-1,96,122,1])
        prediction = model.predict(image)
        return prediction

if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    prediction = import_and_predict(image, model)
    st.write("DIAGNOSIS:")
    if np.argmax(prediction) == 0:
        st.write("HEALTHY")
    else:
        st.write("SICK")
    
    
    st.text("Probability (0: Normal, 1: Sick")
    st.write(prediction)
