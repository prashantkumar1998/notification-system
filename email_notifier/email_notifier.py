import smtplib
from kafka import KafkaConsumer
import json

SENDER_EMAIL_ID = "prashantkrjha04082023@gmail.com"
RECEIVER_EMAIL_ID = "prashantkrjha5@gmail.com"
PASSWORD = "ttzujlocrfoohdfp"

def get_tracking_details(tracking_id):
    '''
    tracking service is independent service
    to get details hit api of tracking service
    '''
    res: dict
    return res

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

    def email_sender(self, message):
        try:
            # sending the mail
            self.smtp.sendmail(SENDER_EMAIL_ID, RECEIVER_EMAIL_ID, message)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    send_email_obj = send_emails()
    email_message_obj = email_message()
    try:
        consumer = KafkaConsumer(
            "email_notification",
            bootstrap_servers='192.168.0.10:9092',
            auto_offset_reset='earliest',
            group_id="email_task_group")
        print("starting the consumer")
        for task_msg in consumer:
            task_msg = json.loads(task_msg.value)
            res = get_tracking_details(task_msg['tracking_id'])
            user = res['name']
            status = res['status']
            noti_msg = email_message_obj.genrate_message(user, status)
            send_email_obj.email_sender(noti_msg)

    except Exception as e:
        print(e)

#smtp.quit()