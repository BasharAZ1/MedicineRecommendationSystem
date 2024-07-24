from flask import render_template, request, redirect, url_for, jsonify
from db import  find_user_by_username, users_collection

from flask_login import login_required
from bson.objectid import ObjectId


def homepage():
    return render_template('login.html')


def symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        return redirect(url_for('predict', symptoms=','.join(selected_symptoms)))
    
    symptoms_list = ['abdominal_pain', 'acidity', 'altered_sensorium', 'anxiety', 'back_pain', 
                     'blackheads', 'bladder_discomfort', 'blister', 'bloody_stool', 
                     'blurred_and_distorted_vision', 'breathlessness', 'bruising', 
                     'burning_micturition', 'chest_pain', 'chills', 'cold_hands_and_feets', 
                     'constipation', 'continuous_feel_of_urine', 'continuous_sneezing', 'cough', 
                     'cramps', 'dark_urine', 'dehydration', 'diarrhoea', 'dischromic_patches', 
                     'distention_of_abdomen', 'dizziness', 'excessive_hunger', 
                     'extra_marital_contacts', 'family_history', 'fatigue', 
                     'foul_smell_of_urine', 'headache', 'high_fever', 'hip_joint_pain', 
                     'indigestion', 'irregular_sugar_level', 'irritation_in_anus', 'joint_pain', 
                     'knee_pain', 'lack_of_concentration', 'lethargy', 'loss_of_appetite', 
                     'loss_of_balance', 'mood_swings', 'movement_stiffness', 'muscle_wasting', 
                     'muscle_weakness', 'nausea', 'neck_pain', 'nodal_skin_eruptions', 'obesity', 
                     'pain_during_bowel_movements', 'pain_in_anal_region', 'painful_walking', 
                     'passage_of_gases', 'patches_in_throat', 'pus_filled_pimples', 
                     'red_sore_around_nose', 'restlessness', 'scurring', 'shivering', 
                     'silver_like_dusting', 'skin_peeling', 'skin_rash', 'small_dents_in_nails', 
                     'spinning_movements', 'spotting_urination', 'stiff_neck', 'stomach_pain', 
                     'sunken_eyes', 'sweating', 'swelling_joints', 'swelling_of_stomach', 
                     'swollen_legs', 'ulcers_on_tongue', 'vomiting', 'watering_from_eyes', 
                     'weakness_in_limbs', 'weakness_of_one_body_side', 'weight_gain', 
                     'weight_loss', 'yellow_crust_ooze', 'yellowing_of_eyes', 'yellowish_skin', 
                     'None', 'itching']
    
    return render_template('symptoms.html', symptoms=symptoms_list)


def submit_symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        print(selected_symptoms)
        return "Symptoms submitted successfully!"