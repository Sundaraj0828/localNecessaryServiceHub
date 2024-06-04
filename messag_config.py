import os
from twilio.rest import Client

import sms_DB

#=====================================Lead time Logs=================================================================
def send_data(msg_data):
    sms_Info = []
    sms_cursor = sms_DB.get_sms_details()
    
    for s in sms_cursor:
        sms_Info.append(s)
        consumer_phone = msg_data['number']
        if sms_Info[0]['Account'] == 'Twilio':
            account_sid = sms_Info[0]['SID']
            auth_token =  sms_Info[0]['Auth_Token']
            
            client = Client(account_sid, auth_token)
            final_message = 'Thank You ' + msg_data['user_name'] + ' ! ' + " for connecting with LTH. Your Registration Id is "+ msg_data['regd_id'] + ' and password is ' + msg_data['password']
			
            prefix = '+91'
            num = prefix + consumer_phone
            message = client.messages.create(
									body=final_message,
									from_='+15855132761',
									to=num
									)
		
        return

