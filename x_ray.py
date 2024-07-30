from flask import render_template, request, redirect, url_for, jsonify
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import pickle
from flask_login import login_required
from bson.objectid import ObjectId
import pandas as pd
from werkzeug.utils import secure_filename
from flask_login import login_required
import os
import cv2



UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = tf.saved_model.load('/Users/basharalli/Desktop/Final_med/MedicineRecommendationSystem/models/lung')

labels = ['Bacterial Pneumonia', 'Corona Virus Disease', 'Normal', 'Tuberculosis', 'Viral Pneumonia']
labels_fracture=['fractured', 'not fractured']
model_fracture = tf.saved_model.load('/Users/basharalli/Desktop/Final_med/MedicineRecommendationSystem/models/fracture/model')
image_size = 150
@login_required
def lung_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            if not file_bytes:
                return jsonify({'error': 'Empty file uploaded'}), 400
            
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, 'wb') as f:
                f.write(file_bytes)
            
            try:
                img = load_img(file_path, target_size=(image_size, image_size))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)  

                y_pred_unseen = model(img_array)
                y_pred_class = np.argmax(y_pred_unseen, axis=1)[0]
                return jsonify({'prediction': labels[y_pred_class]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return render_template('lung_page.html')


@login_required
def bones_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        if file:
            filename = secure_filename(file.filename)
            file_bytes = file.read()
            if not file_bytes:
                return jsonify({'error': 'Empty file uploaded'}), 400
            
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, 'wb') as f:
                f.write(file_bytes)
            
            try:
                img = load_img(file_path, target_size=(image_size, image_size))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)  

                y_pred_unseen = model_fracture(img_array)
                y_pred_class = np.argmax(y_pred_unseen, axis=1)[0]
                return jsonify({'prediction': labels_fracture[y_pred_class]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return render_template('bones_page.html')