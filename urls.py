from views import homepage,symptoms,submit_symptoms,searchmedicine,medicine,search,get_medicine_info,fda_search
from x_ray import lung_page,bones_page
from authentication import register, login, logout


def configure_routes(app):
    app.add_url_rule('/', 'homepage', homepage)
    app.add_url_rule('/register', 'register', register,methods=["POST", "GET"])
    app.add_url_rule('/symptoms', 'symptoms', symptoms,methods=["POST", "GET"])
    app.add_url_rule('/login', 'login', login,methods=["POST", "GET"])
    app.add_url_rule('/submit_symptoms', 'submit_symptoms', submit_symptoms,methods=["POST", "GET"])
    app.add_url_rule('/logout', 'logout', logout,methods=[ "POST","GET"])
    app.add_url_rule('/searchmedicine', 'searchmedicine', searchmedicine,methods=["POST", "GET"])
    app.add_url_rule('/medicine', 'medicine', medicine,methods=["POST", "GET"])
    app.add_url_rule('/search', 'search', search,methods=["GET"])
    app.add_url_rule('/get_medicine_info', 'get_medicine_info', get_medicine_info,methods=["GET"])
    app.add_url_rule('/lung_page', 'lung_page', lung_page,methods=["GET","POST"])
    app.add_url_rule('/bones_page', 'bones_page', bones_page,methods=["GET","POST"])
    app.add_url_rule('/FDA_search', 'fda_search', fda_search,methods=["GET","POST"])


    
    
