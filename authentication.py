from db import add_user, find_user_by_username, check_user_password, users_collection, user_from_dict
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, redirect, flash, session, url_for
from models import  User


@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('homepage'))


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_dict = find_user_by_username(username)
        if user_dict and check_user_password(username, password):
            user = user_from_dict(user_dict)

            session['username'] = user.username
            session['user_id'] = str(user._id)
            session['is_logged_in'] = True
            login_user(user)
            return redirect(url_for('symptoms', user_id=user._id))
        else:
            flash('שם משתמש או סיסמה שגויים')
            return render_template('login.html', username=username)

    return render_template('login.html')


def is_password_legal(password):
    if len(password) < 8:
        return False
    special_characters = "!@#&%()"
    if not any(char in special_characters for char in password):
        return False

    return True


def register():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash("הסיסמאות לא תואמות!")
            return render_template('signup.html', username=username,)
        existing_user = users_collection.find_one({"$or": [{"username": username},]})
        if existing_user:
            flash('שם המשתמש או מספר הטלפון כבר תפוס, אנא בחר שם משתמש אחר.')
            return render_template('signup.html', username=username)

        new_user = User(username=username, password=password)
        add_user(new_user)


        users_collection.update_one({"_id": new_user._id}, {"$set": {"services": new_user.services}})

        return redirect(url_for('homepage'))

    return render_template('signup.html')