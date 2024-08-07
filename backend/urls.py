# backend/urls.py
from views import (
    symptoms, submit_symptoms, searchmedicine, 
    search, get_medicine_info, fda_search,write_drug_search
)
from x_ray import lung_page, bones_page, submitfeedback,getlunglables,getBonelables
from authentication import register, login, logout,session_fet

def configure_routes(app):
    app.add_url_rule('/login', 'login', login, methods=["POST", "GET"])
    app.add_url_rule('/register', 'register', register, methods=["POST", "GET"])
    app.add_url_rule('/session', 'session', session_fet, methods=["POST", "GET"])
    app.add_url_rule('/symptoms', 'symptoms', symptoms, methods=["POST", "GET"])
    app.add_url_rule('/submit_symptoms', 'submit_symptoms', submit_symptoms, methods=["POST", "GET"])
    app.add_url_rule('/logout', 'logout', logout, methods=["POST", "GET"])
    app.add_url_rule('/searchmedicine', 'searchmedicine', searchmedicine, methods=["POST", "GET"])
    app.add_url_rule('/search', 'search', search, methods=["GET"])
    app.add_url_rule('/get_medicine_info', 'get_medicine_info', get_medicine_info, methods=["GET"])
    app.add_url_rule('/Lung', 'lung_page', lung_page, methods=["GET", "POST"])
    app.add_url_rule('/Bones', 'bones_page', bones_page, methods=["GET", "POST"])
    app.add_url_rule('/FDA_search', 'fda_search', fda_search, methods=["GET", "POST"])
    app.add_url_rule('/submitfeedback', 'submitfeedback', submitfeedback, methods=["POST"])
    app.add_url_rule('/Lung-get-labels', 'lung-get-labels', getlunglables, methods=["GET"])
    app.add_url_rule('/Bones-get-labels', 'Bones-get-labels', getBonelables, methods=["GET"])
    app.add_url_rule('/write_drug_search', 'write_drug_search', write_drug_search, methods=["POST"])
