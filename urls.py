from views import homepage,symptoms,submit_symptoms
from authentication import register, login, logout


def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/register', 'register', register,methods=["POST", "GET"])
    app.add_url_rule('/symptoms', 'symptoms', symptoms,methods=["POST", "GET"])
    app.add_url_rule('/login', 'login', login,methods=["POST", "GET"])
    app.add_url_rule('/submit_symptoms', 'submit_symptoms', submit_symptoms,methods=["POST", "GET"])
    app.add_url_rule('/login', 'login', login,methods=["POST", "GET"])
    
    
