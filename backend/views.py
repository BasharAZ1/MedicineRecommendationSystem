
from flask import jsonify, request, redirect, url_for
from db import (
    get_medications_by_disease, get_diets_by_disease, get_workout_df_by_disease,
    get_precautions_by_disease, get_description_by_disease, medications_info_collection,get_user_by_username,
    user_interactions_collection
)
import numpy as np
import pickle
from flask_login import login_required
from flask import jsonify, request, redirect, flash, session, url_for, get_flashed_messages
from bson.objectid import ObjectId
import pandas as pd
import ast
import requests
from confluent_kafka import Producer # Kafka Configuration 




conf = {'bootstrap.servers': 'kafka:9092'}  # Kafka service name and port in Minikube
producer = Producer(conf) 
def delivery_report(err, msg): 
    if err is not None: 
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")
        
        
def send_message(topic, message):
    producer.produce(topic, message, callback=delivery_report) 
    producer.flush()

with open('models/svc_model.pkl', 'rb') as file:
    model = pickle.load(file)
    
symptoms_dict = {'itching': 0, 'skin_rash': 1, 'nodal_skin_eruptions': 2, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'stomach_pain': 7, 'acidity': 8, 'ulcers_on_tongue': 9, 'muscle_wasting': 10, 'vomiting': 11, 'burning_micturition': 12, 'spotting_ urination': 13, 'fatigue': 14, 'weight_gain': 15, 'anxiety': 16, 'cold_hands_and_feets': 17, 'mood_swings': 18, 'weight_loss': 19, 'restlessness': 20, 'lethargy': 21, 'patches_in_throat': 22, 'irregular_sugar_level': 23, 'cough': 24, 'high_fever': 25, 'sunken_eyes': 26, 'breathlessness': 27, 'sweating': 28, 'dehydration': 29, 'indigestion': 30, 'headache': 31, 'yellowish_skin': 32, 'dark_urine': 33, 'nausea': 34, 'loss_of_appetite': 35, 'pain_behind_the_eyes': 36, 'back_pain': 37, 'constipation': 38, 'abdominal_pain': 39, 'diarrhoea': 40, 'mild_fever': 41, 'yellow_urine': 42, 'yellowing_of_eyes': 43, 'acute_liver_failure': 44, 'fluid_overload': 45, 'swelling_of_stomach': 46, 'swelled_lymph_nodes': 47, 'malaise': 48, 'blurred_and_distorted_vision': 49, 'phlegm': 50, 'throat_irritation': 51, 'redness_of_eyes': 52, 'sinus_pressure': 53, 'runny_nose': 54, 'congestion': 55, 'chest_pain': 56, 'weakness_in_limbs': 57, 'fast_heart_rate': 58, 'pain_during_bowel_movements': 59, 'pain_in_anal_region': 60, 'bloody_stool': 61, 'irritation_in_anus': 62, 'neck_pain': 63, 'dizziness': 64, 'cramps': 65, 'bruising': 66, 'obesity': 67, 'swollen_legs': 68, 'swollen_blood_vessels': 69, 'puffy_face_and_eyes': 70, 'enlarged_thyroid': 71, 'brittle_nails': 72, 'swollen_extremeties': 73, 'excessive_hunger': 74, 'extra_marital_contacts': 75, 'drying_and_tingling_lips': 76, 'slurred_speech': 77, 'knee_pain': 78, 'hip_joint_pain': 79, 'muscle_weakness': 80, 'stiff_neck': 81, 'swelling_joints': 82, 'movement_stiffness': 83, 'spinning_movements': 84, 'loss_of_balance': 85, 'unsteadiness': 86, 'weakness_of_one_body_side': 87, 'loss_of_smell': 88, 'bladder_discomfort': 89, 'foul_smell_of urine': 90, 'continuous_feel_of_urine': 91, 'passage_of_gases': 92, 'internal_itching': 93, 'toxic_look_(typhos)': 94, 'depression': 95, 'irritability': 96, 'muscle_pain': 97, 'altered_sensorium': 98, 'red_spots_over_body': 99, 'belly_pain': 100, 'abnormal_menstruation': 101, 'dischromic _patches': 102, 'watering_from_eyes': 103, 'increased_appetite': 104, 'polyuria': 105, 'family_history': 106, 'mucoid_sputum': 107, 'rusty_sputum': 108, 'lack_of_concentration': 109, 'visual_disturbances': 110, 'receiving_blood_transfusion': 111, 'receiving_unsterile_injections': 112, 'coma': 113, 'stomach_bleeding': 114, 'distention_of_abdomen': 115, 'history_of_alcohol_consumption': 116, 'fluid_overload.1': 117, 'blood_in_sputum': 118, 'prominent_veins_on_calf': 119, 'palpitations': 120, 'painful_walking': 121, 'pus_filled_pimples': 122, 'blackheads': 123, 'scurring': 124, 'skin_peeling': 125, 'silver_like_dusting': 126, 'small_dents_in_nails': 127, 'inflammatory_nails': 128, 'blister': 129, 'red_sore_around_nose': 130, 'yellow_crust_ooze': 131}
diseases_dict = {
        15: 'Fungal infection', 4: 'Allergy', 16: 'GERD', 9: 'Chronic cholestasis', 14: 'Drug Reaction',
        33: 'Peptic ulcer disease', 1: 'AIDS', 12: 'Diabetes ', 17: 'Gastroenteritis', 6: 'Bronchial Asthma',
        23: 'Hypertension ', 30: 'Migraine', 7: 'Cervical spondylosis', 32: 'Paralysis (brain hemorrhage)',
        28: 'Jaundice', 29: 'Malaria', 8: 'Chicken pox', 11: 'Dengue', 37: 'Typhoid', 40: 'hepatitis A',
        19: 'Hepatitis B', 20: 'Hepatitis C', 21: 'Hepatitis D', 22: 'Hepatitis E', 3: 'Alcoholic hepatitis',
        36: 'Tuberculosis', 10: 'Common Cold', 34: 'Pneumonia', 13: 'Dimorphic hemmorhoids(piles)', 18: 'Heart attack'
    }


def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list



@login_required
def symptoms():
    symptoms_list = list(symptoms_dict.keys())
    return jsonify(symptoms=symptoms_list)


def submit_symptoms():
    if request.method == 'POST':
        data = request.get_json()
        print("Received data:", data)
        selected_symptoms = data.get('symptoms', [])
        
        if not selected_symptoms:
            return jsonify({"error": "No symptoms provided"}), 400

        prediction = predict_disease(selected_symptoms)
        print("Prediction:", prediction)
        
        if not prediction:
            return jsonify({"error": "Prediction failed"}), 500

        disease = prediction[0]
        diets = get_diets_by_disease(disease)
        medications = get_medications_by_disease(disease)
        workout = get_workout_df_by_disease(disease)
        precautions = get_precautions_by_disease(disease)
        description = get_description_by_disease(disease)
        
        # Ensure diets and medications are properly parsed
        diets = [ast.literal_eval(diet) for diet in diets]
        medications = [ast.literal_eval(medication) for medication in medications]
        diets = flatten(diets)
        medications = flatten(medications)

        response = {
            'predicted_disease': disease,
            'predicted_disease_code': prediction[1],
            'description': description,
            'symptoms': selected_symptoms,
            'medications': medications,
            'precautions': precautions,
            'diet': diets,
            'workout': workout
        }
        response = remove_nan_values(response)

        return jsonify(response)

def remove_nan_values(data):
    if isinstance(data, list):
        return [remove_nan_values(item) for item in data if not (isinstance(item, float) and np.isnan(item))]
    elif isinstance(data, dict):
        return {k: remove_nan_values(v) for k, v in data.items() if not (isinstance(v, float) and np.isnan(v))}
    else:
        return data

def predict_disease(symptoms):
    num_features = 132
    feature_vector = [0] * num_features
    for symptom in symptoms:
        if symptom in symptoms_dict:
            feature_vector[symptoms_dict[symptom]] = 1  
    feature_vector_df = pd.DataFrame([feature_vector], columns=symptoms_dict.keys())
    
    x = model.predict(feature_vector_df)

    if x[0] in diseases_dict:
        x_disease = diseases_dict[x[0]]
    else:
        x_disease = x[0]
    
    return x_disease, x[0]

@login_required
def searchmedicine():
    return jsonify({"message": "Search medicine page"})

@login_required
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify(suggestions=[])

    search_criteria = {
        '$or': [
            {'name': {'$regex': f'^{query}', '$options': 'i'}},
        ]
    }

    suggestions = medications_info_collection.find(search_criteria, {'name': 1})
    suggestions_list = [{'name': s['name'], 'id': str(s['_id'])} for s in suggestions]
    return jsonify(suggestions=suggestions_list)



@login_required
def get_medicine_info():
    med_name = request.args.get('name', '')
    medicine_info = medications_info_collection.find_one({'name': med_name})
    if medicine_info:
        info = {
            'name': medicine_info.get('name', 'N/A'),
            'chemical_class': medicine_info.get('chemicalclass', 'N/A'),
            'habit_forming': medicine_info.get('habitforming', 'N/A'),
            'therapeutic_class': medicine_info.get('therapeuticclass', 'N/A'),
            'action_class': medicine_info.get('actionclass', 'N/A'),
            'substitutes': medicine_info.get('substitutes', []),
            'side_effects': medicine_info.get('sideEffects', []),
            'uses': medicine_info.get('uses', [])
        }
        print(info)
        info = remove_nan_values(info)
        return jsonify(info)
    else:
        return jsonify({"error": "Medicine not found"}), 404

def get_drug_info(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results'][0]
        else:
            return "No results found."
    else:
        return f"Error: {response.status_code}"

def extract_important_info(drug_data):
    important_info = {
        "Brand Name": drug_data.get("openfda", {}).get("brand_name", ["N/A"])[0],
        "Generic Name": drug_data.get("openfda", {}).get("generic_name", ["N/A"])[0],
        "Manufacturer": drug_data.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
        "Active Ingredients": drug_data.get("active_ingredient", ["N/A"]),
        "Purpose": drug_data.get("purpose", ["N/A"]),
        "Indications and Usage": drug_data.get("indications_and_usage", ["N/A"]),
        "Warnings": drug_data.get("warnings", ["N/A"]),
        "Dosage and Administration": drug_data.get("dosage_and_administration", ["N/A"]),
        "Inactive Ingredients": drug_data.get("inactive_ingredient", ["N/A"])
    }
    important_info = remove_nan_values(important_info)
    return important_info

@login_required
def fda_search():
    query = request.args.get('query', '')
    print(query)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    drug_data = get_drug_info(query)
    if isinstance(drug_data, dict):
        send_message('user-interactions', str(query))
        important_info = extract_important_info(drug_data)
        return jsonify(important_info)
    else:
        return jsonify({"error": drug_data}), 404


def write_drug_search():
    data = request.json
    if not data or "message" not in data:
            return jsonify({"error": "Invalid input"}), 400
    try:
            user_interactions_collection.insert_one({"message": data["message"]})
            return jsonify({"status": "success"}), 200
    except Exception as e:
            return jsonify({"error": str(e)}), 500