from flask import Flask
from flask_login import LoginManager
from urls import configure_routes
from flask_session import Session
from bson import ObjectId
from dotenv import load_dotenv
from db import users_collection,user_from_dict
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'session_app1'
Session(app)
 
configure_routes(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return user_from_dict(user_data)
    return None


if __name__ == "__main__":
    app.run('0.0.0.0', port=5005)
    