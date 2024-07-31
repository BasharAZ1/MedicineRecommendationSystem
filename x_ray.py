from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import TFSMLayer
import numpy as np
from werkzeug.utils import secure_filename
from flask_login import login_required
import os



UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models using TFSMLayer for Keras 3 compatibility
model_lung = TFSMLayer('/Users/basharalli/Desktop/Final_med/MedicineRecommendationSystem/models/lung', call_endpoint='serving_default')
model_fracture = TFSMLayer('/Users/basharalli/Desktop/Final_med/MedicineRecommendationSystem/models/fracture/model', call_endpoint='serving_default')

labels = ['Bacterial Pneumonia', 'Corona Virus Disease', 'Normal', 'Tuberculosis', 'Viral Pneumonia']
labels_fracture = ['fractured', 'not fractured']

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
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            try:
                img = load_img(file_path, target_size=(image_size, image_size))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                y_pred_unseen = model_lung(img_array)
                print(y_pred_unseen)
                y_pred_class = np.argmax(y_pred_unseen['dense_2'], axis=1)[0]

                return jsonify({'prediction': labels[y_pred_class]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return render_template('lung_page.html', username=session.get('username'))

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
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            try:
 
                img = load_img(file_path, target_size=(image_size, image_size))
                img_array = img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)

                y_pred_unseen = model_fracture(img_array)
                y_pred_class = np.argmax(y_pred_unseen['dense_5'], axis=1)[0]

                return jsonify({'prediction': labels_fracture[y_pred_class]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    return render_template('bones_page.html', username=session.get('username'))


