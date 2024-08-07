from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import csv
from werkzeug.utils import secure_filename
from flask_login import login_required
import os
from models import model_lung,model_fracture,labels,labels_fracture


image_size = 150
CSV_FILE = 'feedback.csv'
CSV_HEADERS = ['Picture Name', 'Label', 'Comments', 'Prediction']
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
                y_pred_class = np.argmax(y_pred_unseen['dense_2'], axis=1)[0]

                return jsonify({'prediction': labels[y_pred_class]})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    r

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




@login_required
def submitfeedback():
        data = request.get_json()
        picture_name = data.get('pictureName')
        label = data.get('label')
        comments = data.get('comments')
        prediction = data.get('prediction')

        if not picture_name or not label or not comments or not prediction:
            return jsonify({'error': 'Missing data'}), 400

        with open(CSV_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([picture_name, label, comments, prediction])

        return jsonify({'message': 'Feedback submitted successfully'}), 200
    




def getlunglables():
    return jsonify({'labels': labels})
    
def getBonelables():
    return jsonify({'labels': labels_fracture})
