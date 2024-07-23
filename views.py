from flask import render_template, request, redirect, url_for, jsonify
from db import  find_user_by_username, users_collection

from flask_login import login_required
from bson.objectid import ObjectId


def homepage():
    return render_template('login.html')

    