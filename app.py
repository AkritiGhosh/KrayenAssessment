
import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageOps

PAGE_CONFIG = {"page_title":"Garbage Collection.io","page_icon":"chart_with_upwards_trend","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

def output(arr):
  classes = {1:'cardboard', 2:'glass',3:'metal',4:'paper',5:'plastic',6:'trash'}
  return classes[np.argmax(arr)]

def import_and_predict(image_data, model):
    size = (128,128)    
    image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
    image = np.asarray(image)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resize = (cv2.resize(img, dsize=(128, 128),interpolation=cv2.INTER_CUBIC))/255.
    img_reshape = img[np.newaxis,...]
    prediction = output(model.predict(img_reshape))
    return prediction

def load_model(path):
    model=tf.keras.models.load_model(path)
    return model

st.title("Krayen Assessment")
st.subheader('Garbage Collection')
with st.spinner('Model is being loaded..'):
  model=load_model('/content/model.h5')

file = st.file_uploader("Please upload an image", type=["jpg", "png"])
st.set_option('deprecation.showfileUploaderEncoding', False)
if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    predictions = import_and_predict(image, model)
    st.write('Prediction:')
    st.write(predictions)