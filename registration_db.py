from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi



def configure_db():
    global con
    global db_user
    global db_lnsh
    global col_user   
    global col_category
    global col_service

    ca = certifi.where()
    con = MongoClient('mongodb+srv://sraj81791sm:uRpvwRRSY3dgnZnI@cluster0.wlq2tfi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', tlsCAFile = ca)     
    
    db_user = con.user_db
    col_user = db_user.users
    db_lnsh = con.lnsh_db
    col_category = db_lnsh.service_categories
    col_service = db_lnsh.services

def save_user(data):
    global col_user
    configure_db()

    col_user.insert_one(data)
    return

def get_registered_users(mail_id):
    global col_user
    configure_db()
    
    regd_user = col_user.find({'email': mail_id}, {'_id':0})
    return regd_user

def save_category(data):
    global col_category
    configure_db()

    col_category.insert_one(data)
    return

def get_categories():
    global col_category
    configure_db()

    data = col_category.find({}, {'_id':0})
    return data

def delete_cat(cid):
    global col_category
    configure_db()

    col_category.delete_one({'category_id':cid})
    return

def create_service(data):
    global col_service
    configure_db()

    col_service.insert_one(data)
    return

def get_services(uid):
    global col_service
    configure_db()

    data = col_service.find({'user_id': uid},{'_id':0})
    return data