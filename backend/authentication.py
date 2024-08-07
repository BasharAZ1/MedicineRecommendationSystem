from db import add_user, find_user_by_username, check_user_password, users_collection, user_from_dict
from flask_login import login_user, logout_user, login_required,current_user
from flask import jsonify, request, redirect, flash, session, url_for, get_flashed_messages
from models import User
from views import send_message

@login_required
def logout():
    get_flashed_messages()
    session.clear()
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user_dict = find_user_by_username(username)
        if user_dict and check_user_password(username, password):
            user = user_from_dict(user_dict)

            session['username'] = user.username
            session['user_id'] = str(user._id)
            session['is_logged_in'] = True
            login_user(user)
            send_message('login', str({username}))
            return jsonify({"message": "Login successful", "user_id": str(user._id)}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"error": "Method not allowed"}), 405

def is_password_legal(password):
    if len(password) < 8:
        return False
    special_characters = "!@#&%()"
    if not any(char in special_characters for char in password):
        return False

    return True

def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        if not is_password_legal(password):
            return jsonify({"error": "Password does not meet the criteria"}), 400

        existing_user = find_user_by_username(username)
        if existing_user:
            return jsonify({"error": "Username already taken"}), 409

        new_user = User(username=username, password=password)
        add_user(new_user)

        session['username'] = new_user.username
        session['user_id'] = str(new_user._id)
        session['is_logged_in'] = True
        login_user(new_user)

        return jsonify({"message": "Registration successful"}), 201

    return jsonify({"error": "Method not allowed"}), 405

def session_fet():
    if 'is_logged_in' in session and session['is_logged_in']:
        return jsonify({"is_logged_in": True, "username": session.get('username')}), 200
    else:
        return jsonify({"is_logged_in": False}), 401



    