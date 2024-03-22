import smtplib
from kafka import KafkaConsumer
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOPIC_NOTIFICATION_IN = "notification_handler"
TOPIC_NOTIFICATION_EMAIL = 'email_notification'
BOOTSTRAP_SERVERS = 'kafka:9092'
#BOOTSTRAP_SERVERS = 'localhost:9092'
CONSUMER_GROUP_EMAIL = 'email_consumer_group'

SENDER_EMAIL_ID = os.getenv("SENDER_EMAIL_ID")
PASSWORD = os.getenv("PASSWORD")

def get_tracking_details(tracking_id):
    '''
    tracking service is independent service
    to get details hit api of tracking service
    '''
    payload = {
        "tracking_id": tracking_id,
    }

    headers = {
        "Content-Type": "application/json"
    }

    url = os.getenv("url")

    try:
        resp = requests.get(url, headers=headers, params = payload).json()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

    return resp

class email_message():
    def __init__(self):
        self.status_message_map = {
            "ordered":"hy {}, your order has been placed",
            "dispatched":"hy {}, your order has been dispatched",
            "shiped":"hy {}, your order has been shiped",
            "out_for_delivery":"hy {}, your order is out for delivery",
            "delivered":"hy {}, your order has been delivered",
            "picked_up":"hy {}, your item has been picked",
            "return_to_seller":"hy {}, your item is return to seller",
            "undelivered":"hy {}, your order is undelivered"
        }
    def genrate_message(self, user_name, status):
        msg = self.status_message_map[status]
        return msg.format(user_name)
    

class send_emails():
    def __init__(self):
        try:
            self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
            self.smtp.starttls()
            self.smtp.login(SENDER_EMAIL_ID, PASSWORD)
        except Exception as e:
            print(e)

    def email_sender(self, message, receiver_email):
        try:
            # sending the mail
            print('----------sending email--------------------')
            self.smtp.sendmail(SENDER_EMAIL_ID, receiver_email, message)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    send_email_obj = send_emails()
    email_message_obj = email_message()
    try:
        consumer = KafkaConsumer(
            TOPIC_NOTIFICATION_EMAIL,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            )

        print("starting the consumer")
        for task_msg in consumer:
            #import pdb;pdb.set_trace()
            task_msg = json.loads(task_msg.value)
            print(f'---------{task_msg}-----------------')
            res = get_tracking_details(task_msg['tracking_id'])
            user = res['name']
            email = res['email']
            status = res['status']
            print('-------sending email notification--------------')
            noti_msg = email_message_obj.genrate_message(user, status)
            send_email_obj.email_sender(noti_msg, email)

        smtp.quit()

    except Exception as e:
        print(e)