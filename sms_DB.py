from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi

def configure_db():
    global con
    global db_msg
    global col_msgInfo

    ca = certifi.where()
    con = MongoClient('')           
    db_msg = con.config_data_DB
    col_msgInfo = db_msg.sms_config


def get_sms_details():
    global col_msgInfo
    configure_db()

    data = col_msgInfo.find({}, {'_id':0})
    return data

def add_sensitive_info(data):
    global col_msgInfo
    configure_db()

    col_msgInfo.insert_one(data)
    return
