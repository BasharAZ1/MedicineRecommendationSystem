from models import check_password_hash
from models import User
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_cluster_url = os.getenv('MONGO_CLUSTER_URL')

mongo_uri = f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster_url}/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
userdb = client['userdb']
users_collection = userdb['users']
medications_collection = userdb['medications']
diets_collection = userdb['diets']
workout_collection = userdb['workout']
precautions_collection = userdb['precautions']
Description_collection = userdb['Description']
medications_info_collection=userdb['medications_info']
user_interactions_collection=userdb['user_interactions']





def split_csv(file_path, chunk_size):
    if not os.path.exists('chunks'):
        os.makedirs('chunks')
    for i, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        chunk.to_csv(f'chunks/chunk_{i}.csv', index=False)


def upload_csv_to_mongodb(collection, csv_file):

    df = pd.read_csv(csv_file)
    data = df.to_dict(orient='records')
    collection.insert_many(data)
    
    
    
def upload_chunks(file_path, chunk_size, collection):
    split_csv(file_path, chunk_size)
    chunk_files = [f'chunks/{f}' for f in os.listdir('chunks') if f.endswith('.csv')]
    for chunk_file in chunk_files:
        upload_csv_to_mongodb(collection, chunk_file)
        print(f"Uploaded {chunk_file} to MongoDB")
def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "services": user.services
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)


def get_medications_by_disease(disease):
    medications = medications_collection.find({"Disease": disease})
    return [medication.get('Medication') for medication in medications]


def get_diets_by_disease(disease):
    diets = diets_collection.find({"Disease": disease})
    return [diet.get('Diet') for diet in diets]



def get_workout_df_by_disease(disease):
    workouts = workout_collection.find({"disease": disease})
    return [workout.get('workout') for workout in workouts]



def get_precautions_by_disease(disease):
    result = precautions_collection.find_one({"Disease": disease})
    if result:
        return [result.get('Precaution_1'), result.get('Precaution_2'), result.get('Precaution_3'), result.get('Precaution_4')]
    else:
        return None
    
def get_description_by_disease(disease):
    result = Description_collection.find_one({"Disease": disease})
    if result:
        return result.get("Description")
    else:
        return "Not found"




def find_user_by_username(username):
    return users_collection.find_one({"username": username})


def check_user_password(username, password):
    user = find_user_by_username(username)
    if user and check_password_hash(user['password_hash'], password):
        return True
    return False


def user_from_dict(user_dict):
    user = User(
        username=user_dict['username'],
        password=user_dict['password_hash'],
    )
    user.set_id(user_dict['_id'])
    user.services = user_dict['services']
    return user

def get_user_by_username(username):
    # Implement this function to retrieve user details from your database
    user = User.query.filter_by(username=username).first()
    return user


