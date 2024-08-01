from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import TFSMLayer
import numpy as np
import csv
from werkzeug.utils import secure_filename
from flask_login import login_required
import os

CSV_FILE = 'feedback.csv'
CSV_HEADERS = ['Picture Name', 'Label', 'Comments', 'Prediction']
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models using TFSMLayer for Keras 3 compatibility
model_lung = TFSMLayer('models/lung', call_endpoint='serving_default')
model_fracture = TFSMLayer('models/fracture/model', call_endpoint='serving_default')
# model_brain = load_model('models/Brain/my_model.keras')

labels = ['Bacterial Pneumonia', 'Corona Virus Disease', 'Normal', 'Tuberculosis', 'Viral Pneumonia']
labels_fracture = ['fractured', 'not fractured']
# labels_tumor=["No Tumor","Tumor"]

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
    
    return render_template('xray.html', username=session.get('username'),h1_content='Lung Check',labels=labels)

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
    
    return render_template('xray.html', username=session.get('username'),h1_content='Brain Check',labels=labels_fracture)


# @login_required
# def brain_page():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(file_path)
            
#             try:
    
#                         img = load_img(file_path, target_size=(224, 224))
#                         img_array = img_to_array(img)
#                         img_array = np.expand_dims(img_array, axis=0) 

#                         y_pred_unseen = model_brain.predict(img_array)
#                         y_pred_class = np.argmax(y_pred_unseen, axis=1)[0]

#                         return jsonify({'prediction': labels_tumor[y_pred_class]})
#             except Exception as e:
#                         return jsonify({'error': str(e)}), 500  
    
#     return render_template('xray.html', username=session.get('username'),h1_content='Brain Tumor',labels=labels_tumor)



def feedback():
    feedback = request.json
    picture_name = feedback.get('pictureName')
    label = feedback.get('label')
    comments = feedback.get('comments')
    prediction = feedback.get('prediction')
    
    # Write feedback to CSV file
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([picture_name, label, comments, prediction])

    return jsonify({'status': 'success'}), 200