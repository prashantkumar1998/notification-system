import smtplib
from kafka import KafkaConsumer
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
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
            "ordered":"hy {user}, your order has been placed",
            "dispatched":"hy {user}, your order has been dispatched",
            "shiped":"hy {user}, your order has been shiped",
            "out_for_delivery":"hy {user}, your order is out for delivery",
            "delivered":"hy {user}, your order has been delivered",
            "picked_up":"hy {user}, your item has been picked",
            "return_to_seller":"hy {user}, your item is return to seller",
            "undelivered":"hy {user}, your order is undelivered"
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
            self.smtp.sendmail(SENDER_EMAIL_ID, receiver_email, message)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    send_email_obj = send_emails()
    email_message_obj = email_message()
    try:
        consumer = KafkaConsumer(
            "email_notification",
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id="email_task_group")

        print("starting the consumer")
        for task_msg in consumer:
            task_msg = json.loads(task_msg.value)
            res = get_tracking_details(task_msg['tracking_id'])
            user = res['name']
            email = res['email']
            status = res['status']
            noti_msg = email_message_obj.genrate_message(user, status)
            send_email_obj.email_sender(noti_msg, email)

        smtp.quit()

    except Exception as e:
        print(e)