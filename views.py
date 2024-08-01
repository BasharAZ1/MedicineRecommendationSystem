from flask import render_template, request, redirect, url_for, jsonify
from db import   get_medications_by_disease,get_diets_by_disease,get_workout_df_by_disease,get_precautions_by_disease,get_description_by_disease,medications_info_collection,symptoms_collection,diseases_collection
import numpy as np
import pickle
from flask_login import login_required
from bson.objectid import ObjectId
import pandas as pd
from werkzeug.utils import secure_filename
import os
import ast
import requests


with open('models/svc_model.pkl', 'rb') as file:
    model = pickle.load(file)
    
def build_dict(collection):
    name_id_dict = {}
    documents = collection.find()
    for document in documents:
        name = document['name']
        id_ = document['id']
        name_id_dict[name] = id_

    return name_id_dict
def build_dict_dis(collection):
    name_id_dict = {}
    documents = collection.find()
    for document in documents:
        id_ = document['id']
        name = document['name']
        name_id_dict[id_] = name

    return name_id_dict


symptoms_dict=build_dict(symptoms_collection)
diseases_dict=build_dict_dis(diseases_collection)



def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list



@login_required
def homepage(): 
    return render_template('index.html')

@login_required
def symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        return redirect(url_for('predict', symptoms=','.join(selected_symptoms)))
    symptoms_list=list(symptoms_dict.keys())
    return render_template('symptoms.html', symptoms=symptoms_list)

@login_required
def submit_symptoms():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        prediction = predict_disease(selected_symptoms)
        disease = prediction[0]
        diets=get_diets_by_disease(disease)
        medactions=get_medications_by_disease(disease)
        workout=get_workout_df_by_disease(disease)
        precautions=get_precautions_by_disease(disease)
        Description=get_description_by_disease(disease)
        diets = [ast.literal_eval(diet) for diet in diets]
        medactions=[ast.literal_eval(medaction) for medaction in medactions]
        diets = flatten(diets)
        medactions=flatten(medactions)
        
        return render_template('Disease.html', predicted_disease=disease, predicted_disease_code=prediction[1],
                               description=Description, 
                               symptoms=selected_symptoms, medications=medactions, precautions=precautions,
                               diet=diets, workout=workout)
    
# @login_required   
# def predict_disease(symptoms):
#     num_features = 132
#     feature_vector = [0] * num_features
#     for symptom in symptoms:
#         if symptom in symptoms_dict:
#             feature_vector[symptoms_dict[symptom]] = 1  
#     x = model.predict([feature_vector]) 
#     if x[0] in diseases_dict:
#         x_disease = diseases_dict[x[0]]
#     else:
#         x_disease = (x[0])  
#     return x_disease, x[0]

@login_required
def predict_disease(symptoms):
    num_features = 132
    feature_vector = [0] * num_features
    for symptom in symptoms:
        if symptom in symptoms_dict:
            feature_vector[symptoms_dict[symptom]] = 1  

    # Create a DataFrame with the correct feature names
    feature_vector_df = pd.DataFrame([feature_vector], columns=symptoms_dict.keys())
    
    x = model.predict(feature_vector_df)

    if x[0] in diseases_dict:
        x_disease = diseases_dict[x[0]]
    else:
        x_disease = x[0]

    return x_disease, x[0]

@login_required
def searchmedicine():
    return render_template('medicnices.html')

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
def medicine():
    if request.method == 'POST':
        pass 
    return render_template('medicine.html')
    
    
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
    return important_info

def fda_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    drug_data = get_drug_info(query)
    if isinstance(drug_data, dict):
        important_info = extract_important_info(drug_data)
        return jsonify(important_info)
    else:
        return jsonify({"error": drug_data}), 404


