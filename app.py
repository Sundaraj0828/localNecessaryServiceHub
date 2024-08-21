from flask import Flask, redirect, render_template, url_for, request, flash, session, Response
from functools import wraps
from passlib.hash import sha256_crypt




import random
import string

from datetime import datetime

import registration_db
import constructor

# hello

app = Flask(__name__)
app.secret_key = "lnsh123456-proj2k23"

# =======================================================================
# =======================================================================


# --------------------------encryption of password --------------
def sha_encryption(un_encrypted_password):
    encrypted_password = sha256_crypt.encrypt(un_encrypted_password)
    return encrypted_password 
# ------------------------generate random id----------------------------------
def generate_id(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_uppercase) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string

def generate_id_with_fixedChars(letters, digits_count):
    sample_str = letters
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))
    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string

# -----------------------end of random id generator---------------------------

# ================================Login Section
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'username' in session:
      return f(*args, **kwargs)
    else:
      return redirect(url_for('login'))
  return wrap

@app.route("/sign_out")
@login_required
def sign_out():
    session.clear()
    response = Response()
    response.cache_control.s_maxage = 1
    return redirect(url_for('home'))

@app.route('/signin/')
def login():
    user_exists_flag = False
    if 'username' in session:
        user_exists_flag = True
        session['page'] = ''
        return redirect(url_for('home'))
    else:
        user_exists_flag = False
        return render_template('sign-in.html', username = '', user_exists = user_exists_flag)

@app.route("/login/attempt", methods=['POST'])
def login_attempt():
    db_auth_data = {}
    incorrect_pass_flag = False

    # ==================get form data
    login_id = request.form['email'].strip()
    login_pswd = request.form['password'].strip()

    cursor = registration_db.get_registered_users(login_id) 
    for i in cursor:
        db_auth_data = i

    print(db_auth_data)

    if db_auth_data:
        if sha256_crypt.verify(login_pswd, db_auth_data['password']):
            session['username'] = db_auth_data['f_name'] + ' ' + db_auth_data['l_name']
            session['first_name'] = db_auth_data['f_name']
            session['user_email'] = db_auth_data['email']
            session['user_type'] = db_auth_data['user_type']
            session['user_id'] = db_auth_data['user_id']
            session['contact_num'] = db_auth_data['number']
            session['address'] = db_auth_data['address']  
            session['flag'] = '' 
            session.pop('_flashes', None)
            session.permanent = False
        else:
            incorrect_pass_flag = True
            flash('Invalid password !! Check your password', 'error')
    else:
        incorrect_pass_flag = True
        flash('User not exists !! Register yourself first', 'error')
    return redirect(url_for('login'))

@app.route('/')
# @login_required
def home():
    try:
        if session:
            if session['user_type'] == 'Management':
                session['flag'] = 'Management'
                return redirect(url_for('management_home'))
            elif session['user_type'] == 'Business':
                session['flag'] = 'Business'
                return redirect(url_for('business_home'))
            elif session['user_type'] == 'Customer':
                session['flag'] = 'Customer'
                return redirect(url_for('customer_home'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    except:
        flash("Login ")
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))



# add service catagory
@app.route('/add_category', methods=['POST'])
def add_category():
    data = {}
    cname = request.form['category'].strip().upper()
    name_chars = cname[:3:2]
    data['category_name'] = cname
    data['category_id'] = generate_id_with_fixedChars(name_chars, 5)
    data['category_added_date'] = datetime.now()

    registration_db.save_category(data)
    return redirect(url_for('home'))

# add service location center point
@app.route('/add_location_centers', methods=['POST'])
def add_location_centers():
    data = {}
    lname = request.form['location_center'].strip().upper()
    name_chars = lname[:3:2]
    data['location'] = lname
    data['location_id'] = generate_id_with_fixedChars(name_chars, 5)
    data['location_added_date'] = datetime.now()

    registration_db.save_location_center_point(data)
    return redirect(url_for('home'))

@app.route('/view_all_service_categories')
def view_all_service_categories():
    session['flag'] = 'services'
    category_list = []
    cursor = registration_db.get_categories()
    for i in cursor:
        i['category_added_date'] = i['category_added_date'].strftime('%d-%b-%Y')
        category_list.append(i)

    
    
    return render_template('service_categories.html', cat = category_list)

@app.route('/signup')
def signup():
    return render_template('sign-up.html')

@app.route('/dashboard')
def dashboard():
    session['flag'] = 'dashboard'
    return render_template('dashboard.html')

@app.route('/management_home')
def management_home():
    cat_list = []
    location_list = []
    cursor = registration_db.get_categories()
    cursor2 = registration_db.get_all_locations()
    for i in cursor:
        cat_list.append(i)
    for l in cursor2:
        location_list.append(l)
    return render_template('homepage_mg.html', cat = cat_list, loc = location_list)

@app.route('/business_home')
def business_home():
    service_list = []
    cat_list = []
    cursor = registration_db.get_categories()

    for i in cursor:
        cat_list.append(i)
    try:
        cursor_services = registration_db.get_services(session['user_id'])
    except Exception as e:
        print(e)
        msg = "Session Expired"
        flash(msg)
        return redirect(url_for("error_page"))
    else:        
        for c in cursor_services:
            service_list.append(c)
        
        service_count = len(service_list)
        return render_template('business_home.html', cat = cat_list, services = service_list, s_count = service_count)

@app.route('/customer_home')
def customer_home():
    return render_template('customer_home.html')

@app.route('/register', methods=['POST'])
def register():
    user_data = []
    data = constructor.get_form_data()

    email = data['email']
    cursor = registration_db.get_registered_users(email)
    for i in cursor:
        user_data.append(i)
        
    if len(user_data):
        print('user exist')
        return redirect(url_for('signup'))
    else:
    # id generate
        u_type = data['user_type'][:2].upper()
        char_part = 'LNSH23'+u_type+'-'
        u_id = generate_id_with_fixedChars(char_part, 5)
        data['user_id'] = u_id
        # data['registration_date'] = datetime.datetime.today()
        data['registration_date'] = datetime.now()
        pswd = data['password']
        encrypted_pswd = sha_encryption(pswd)
        data['password'] = encrypted_pswd 
        
        registration_db.save_user(data)

        return redirect(url_for('login'))

# app.route('/')
# def add_sensitive_info


@app.route('/delete_category/<cid>')
def delete_category(cid):
    registration_db.delete_cat(cid)
    return redirect(url_for('home'))

@app.route('/delete_location/<loc_id>')
def delete_location(loc_id):
    registration_db.delete_location(loc_id)
    return redirect(url_for('home'))

@app.route("/error_page")
def error_page():
    return render_template('error_page.html')

@app.route('/add_service', methods=['POST'])
def add_service():
    form_data = {}
    form_data['service'] = request.form['service']
    form_data['vendor'] = request.form['vendor']
    form_data['category'] = request.form['category']
    form_data['service_id'] = generate_id_with_fixedChars('LNS-S-', 5)
    form_data['service_added_date'] = datetime.now()
    try:
        form_data['user_id'] = session['user_id']
    except Exception as e:
        print(e.args)
        flash("Session Expired!! To add service, login first")
        return redirect(url_for("error_page"))
    
    return redirect(url_for('home'))

@login_required
@app.route('/profile')
def profile():
    user = []
    category_list = []
    email = session['user_email']    
    cursor = registration_db.get_registered_users(email)
    for i in cursor:
        user.append(i)
        
    cat_cursor = registration_db.get_categories()
    for c in cat_cursor:
        category_list.append(c)
        
    
    
    
    return render_template('profile.html', user = user, cat = category_list)

# ========================== End of Logic Section ============================== 
if __name__ == '__main__':
    app.run(debug=True)