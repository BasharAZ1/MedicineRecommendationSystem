from models import check_password_hash
from models import User
from pymongo import MongoClient
from dotenv import load_dotenv
import os

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





def add_user(user):
    user_data = {
        "username": user.username,
        "password_hash": user.password_hash,
        "services": user.services
    }
    result = users_collection.insert_one(user_data)
    user.set_id(result.inserted_id)





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



