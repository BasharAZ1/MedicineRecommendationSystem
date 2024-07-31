from pymongo import MongoClient, TEXT
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# Retrieve MongoDB credentials from environment variables
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_cluster_url = os.getenv('MONGO_CLUSTER_URL')
mongo_uri = f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster_url}/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
userdb = client['userdb']
symptoms_collection = userdb['symptoms']
diseases_collection=userdb['diseases']

name_id_dict = {}
documents = symptoms_collection.find()
for document in documents:
    name = document['name']
    id_ = document['id']
    name_id_dict[name] = id_

# Print the dictionary
print(name_id_dict)