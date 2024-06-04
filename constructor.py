from flask import request

def get_form_data():
    form_data = {}
    
    form_data['f_name'] = request.form['f_name'].strip().capitalize()
    form_data['l_name'] = request.form['l_name'].strip().capitalize()
    form_data['address'] = request.form['address'].strip().capitalize()
    form_data['number'] = request.form['number'].strip().capitalize()
    form_data['email'] = request.form['email_id'].strip()
    form_data['password'] = request.form['password'].strip()
    form_data['user_type'] = request.form['userType']
    form_data['Terms_conditions'] = request.form.get('tnc')
    
    return form_data