from views import homepage
from authentication import register, login, logout


def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/register', 'register', register,methods=["POST", "GET"])
    
