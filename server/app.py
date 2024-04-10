from flask import *
app = Flask(__name__)

import db_services 


@app.route('/sign_up_user', methods={'POST'})
def sign_up_user():

    """
    to sign up a new user
    """
    data = request.get_json()
    user_name = data['user_name']
    user_pass = data['user_pass']

    result = db_services.sign_up_user(user_name = user_name,user_pass = user_pass)
    
    return jsonify(result)