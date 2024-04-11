from flask import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

import db_services
from session_management import * 

@app.route('/', methods={'GET', 'POST'})
def welcome():

    result = {'success': 0, 'message':'hello'}
    
    return jsonify(result)

@app.route('/sign_up_user', methods={'POST'})
def sign_up_user():

    """
    to sign up a new user
    """
    data = request.get_json()
    name = data['name']
    user_name = data['user_name']
    user_pass = data['user_pass']

    result = db_services.sign_up_user(name = name, user_name = user_name, user_pass = user_pass)
    
    return jsonify(result)

@app.route('/login', methods={'POST', 'GET'})
def login():

    """
    to login a user
    """
    
    data = request.get_json()
    user_name = data['user_name']
    user_pass = data['user_pass']
    
    result = db_services.login(user_name = user_name, user_pass = user_pass)
    
    if result['success'] == 1:
        logged_in = True
        current_user = result['user_id']
        if db_services.is_manager(current_user):
            role.append('M')
        if db_services.is_sales_clerk(current_user):
            role.append('S')
        if db_services.is_inventory_clerk(current_user):
            role.append('I')
    
    return jsonify(result)

@app.route('/logout', methods={'POST'})
def logout():

    """
    to logout a user
    """
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
    else:
        logged_in = False
        current_user = None
        role = None
        result = {'success': 1, 'status': 'User successfully logged out'}
    
    return jsonify(result)

@app.route('/profile', methods={'POST'})
def profile():

    """
    to show profile details of a user
    """
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
    else:
        result = db_services.profile(user_id = current_user)
    
    return jsonify(result)

@app.route('/about', methods={'POST'})
def about():

    """
    about page of service
    """

    return render_template("display.html", account=account)


@app.route('/sales_stats', methods={'POST'})
def sales_stats():

    """
    to show sales statistics
    """
    
    data = request.get_json()
    start_date = data['start_date']
    end_date = data['end_date']
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
        
    elif 'M' not in role:
        result = {'success': 0, 'status': 'You do not have access privileges'}
    else:
        result = db_services.sales_statistics(start_date = start_date, end_date = end_date)
    
    return jsonify(result)

#add billing data

@app.route('/inventory', methods={'POST'})
def inv_view():

    """
    to show inventory
    """
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
        
    elif 'M' not in role and 'I' not in role:
        result = {'success': 0, 'status': 'You do not have access privileges'}
    else:
        result = db_services.inventory_view()
    
    return jsonify(result)

@app.route('/update_quantity', methods={'POST'})
def inv_q_update():

    """
    to update inventory quantities
    """
    data = request.get_json()
    item_code = data['item_code']
    quantity = data['quantity']
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
        
    elif 'M' not in role and 'I' not in role:
        result = {'success': 0, 'status': 'You do not have access privileges'}
    else:
        result = db_services.inventory_update(item_code = item_code, qty = quantity)
    
    return jsonify(result)

@app.route('/update_price', methods={'POST'})
def inv_p_update():

    """
    to update inventory item prices
    """
    data = request.get_json()
    item_code = data['item_code']
    price = data['price']
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
        
    elif 'M' not in role and 'I' not in role:
        result = {'success': 0, 'status': 'You do not have access privileges'}
    else:
        result = db_services.price_update(item_code = item_code, new_price = price)
    
    return jsonify(result)

@app.route('/inventory_add', methods={'POST'})
def inv_add():

    """
    to add new items to inventory
    """
    data = request.get_json()
    item_name = data['item_name']
    quantity = data['quantity']
    unit_price = data['unit_price']
    unit_cost = data['unit_cost']
    
    if not logged_in:
        result = {'success': 0, 'status': 'User must be logged in first to log out'}
        
    elif 'M' not in role:
        result = {'success': 0, 'status': 'You do not have access privileges'}
    else:
        result = db_services.add_item(item_name = item_name, quantity = quantity, unit_price = unit_price, unit_cost = unit_cost)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True)
