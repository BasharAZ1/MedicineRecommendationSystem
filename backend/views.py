
from flask import jsonify, request
from db import (
    get_medications_by_disease, get_diets_by_disease, get_workout_df_by_disease,
    get_precautions_by_disease, get_description_by_disease, medications_info_collection,
    userdb
)
from models import symptoms_dict,diseases_dict,model,producer,delivery_report
import numpy as np

from flask_login import login_required
from bson.objectid import ObjectId
import pandas as pd
import ast
import requests





        
        
def send_message(topic, message):
    producer.produce(topic, message, callback=delivery_report) 
    producer.flush()





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
        send_message('drug', str(query))
        important_info = extract_important_info(drug_data)
        return jsonify(important_info)
    else:
        return jsonify({"error": drug_data}), 404


def write_interactions():
    data = request.json
    if not data or "message" not in data or "topic" not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    topic = data["topic"]
    message = data["message"]
    
    try:
        collection_name = topic + "_interactions"
        if collection_name not in userdb.list_collection_names():
            userdb.create_collection(collection_name)
        
        collection = userdb[collection_name]
        collection.insert_one({"message": message})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    

def drugs_data_fetch():
    collection_name = "drug_interactions"
    collection = userdb[collection_name]
    results = collection.find({}, {"_id": 0, "message": 1}) 
    searched_drugs = {}
    for result in results:
        drug = result['message']
        if drug in searched_drugs:
            searched_drugs[drug] += 1
        else:
            searched_drugs[drug] = 1
    return jsonify(searched_drugs)