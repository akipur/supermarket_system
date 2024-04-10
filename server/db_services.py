import datetime
from db_connector import *
from classes import *
from session_management import *

def sign_up_user(name, user_name, user_pass) -> str:
    """Inserts user data into database for new user being registered

    Args:
        user_name (str): name of user
        user_pass (str): password for user login

    Returns:
        str: message of failure/success in adding new user
    """
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    
    insert_query = "INSERT INTO User(name, user_name, user_pass, join_date) VALUES(%s, %s, %s, CURDATE())"
    
    try:
        cur.execute(insert_query, (name, user_name, user_pass))
        db_connection.commit()
        
    except:
        return {'status': False, 'error': "Failed to insert"}
    
    result = "Sign-Up Done"
    
    return result

def login(user_name, user_pass) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT user_id FROM user WHERE user_name=%s and user_pass=%s"
    cur.execute(query, (user_name, user_pass))
    row = cur.fetchall()
    
    if len(row) == 0:
        result = {'success': 0, 'status': 'User not found. Please enter correct Username and Password.'}
    
    else:
        user_id = row[0]
        result = {'success': 1, 'status': 'Login Successful', 'user_id': user_id}
        #update session_management in app.py
        
    return result

def is_manager(user_id) -> bool:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT user_id FROM managers WHERE user_id = %s"
    cur.execute(query, (user_id))
    row = cur.fetchall()
    if len(row) == 0:
        return False
    return True

def is_sales_clerk(user_id) -> bool:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT user_id FROM sales_clerks WHERE user_id = %s"
    cur.execute(query, (user_id))
    row = cur.fetchall()
    if len(row) == 0:
        return False
    return True

def is_inventory_clerk(user_id) -> bool:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT user_id FROM inventory_clerks WHERE user_id = %s"
    cur.execute(query, (user_id))
    row = cur.fetchall()
    if len(row) == 0:
        return False
    return True
    
def profile(user_id) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT name, user_name, join_date FROM user WHERE user_id = %s"
    cur.execute(query, (user_id))
    row = cur.fetchall()
    
    if len(row) == 0:
        result = {'success': 0, 'status': 'Some error occured. Please try again later.'}
        
    else:
        result = {'success': 1, 'status': 'User details found.', 'data': {
            'name': row[0],
            'user_name': row[1],
            'join_date': row[2],
            'role': role
            }
        }
        
    return result
    
def sales_statistics(start_date, end_date) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT item_code, item_name, quantity as qty, SUM(quantity * unit_price) as amount, SUM(quantity * (unit_price - unit_cost)) as profit FROM sales GROUP BY item_code where date >= %s and date <= %s"
    cur.execute(query, (start_date, end_date))
    row = cur.fetchall()

    if len(row) == 0:
        result = {'success': 0, 'status': 'Unable to fetch sales data.'}
        
    else:
        result = {'success': 1, 'status': 'Genrerated sales statistics.', 'data': row}
        
    return result

# def billing(bill) -> dict:

#     bill['date'] = datetime.now()
#     bill_items = []
    
#     db_connection = get_db_connection()
    
#     for i in range(int(bill['num_items'])):  
#         cur = db_connection.cursor()
#         cur.execute("SELECT * FROM items WHERE item_code = %s", (bill['code_' + str(i)],))
#         row = cur.fetchone()
#         cur.execute("UPDATE items SET quantity = quantity - %s WHERE item_code = %s", (int(bill['qty_' + str(i)]), bill['code_' + str(i)]))
#         cur.execute("INSERT into sales(sale_date, item_code, item_name, quantity, unit_price, unit_cost) VALUES(%s, %s, %s, %s, %s, %s)")
#         db_connection.commit()
#         cur.close()

#         bill_items.append({
#             'item_code': bill['code_' + str(i)],
#             'name': row['item_name'],
#             'quantity': int(bill['qty_' + str(i)]),
#             'unit_price': float(bill['price_' + str(i)])
#         })

#         sales.insert_one({
#             'item_code': bill['code_' + str(i)],
#             'item_name': row['item_name'],
#             'unit_price': float(bill['price_' + str(i)]),
#             'quantity': int(bill['qty_' + str(i)]),
#             'date': datetime.now()
#         })

#     bills.insert_one({
#         'items': bill_items,
#         'total_cost': float(bill['sub_total']),
#         'date': bill['date']
#     })

#     bill['id'] = bills.count_documents({})
#     bill['bill_items'] = bill_items

def inventory_view() -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "SELECT * from items"
    cur.execute(query)
    row = cur.fetchall()

    if len(row) == 0:
        result = {'success': 0, 'status': 'Unable to fetch inventory data.'}
        
    else:
        result = {'success': 1, 'status': 'Genrerated inventory details.', 'data': row}
        
    return result

def inventory_update(item_code, qty) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "UPDATE items SET quantity = quantity + %s where item_code = %s"
    cur.execute(query, (qty, item_code))
    db_connection.commit()
    query = "SELECT * from items where item_code = %s"
    cur.execute(query, (item_code))
    row = cur.fetchall()

    if len(row) == 0:
        result = {'success': 0, 'status': 'Some error occured.'}
        
    else:
        result = {'success': 1, 'status': 'Updated item inventory', 'data': row}
        
    return result

def price_update(item_code, new_price) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "UPDATE items SET unit_price = %s where item_code = %s"
    cur.execute(query, (new_price, item_code))
    db_connection.commit()
    query = "SELECT * from items where item_code = %s"
    cur.execute(query, (item_code))
    row = cur.fetchall()

    if len(row) == 0:
        result = {'success': 0, 'status': 'Some error occured.'}
        
    else:
        result = {'success': 1, 'status': 'Updated item price.', 'data': row}
        
    return result

def add_item(item_name, quantity, unit_price, unit_cost) -> dict:
    db_connection = get_db_connection()
    cur = db_connection.cursor()
    query = "INSERT into items(item_name, quantity, unit_price, unit_cost) values(%s, %s, %s, %s)"
    cur.execute(query, (item_name, quantity, unit_price, unit_cost))
    db_connection.commit()
    query = "SELECT * from items"
    cur.execute(query)
    row = cur.fetchall()

    if len(row) == 0:
        result = {'success': 0, 'status': 'Some error occured.'}
        
    else:
        result = {'success': 1, 'status': 'Updated inventory.', 'data': row}
        
    return result
        
