from kafka import KafkaConsumer, KafkaProducer
import json
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOPIC_NOTIFICATION_IN = "notification_handler"
TOPIC_NOTIFICATION_EMAIL = 'email_notification'
BOOTSTRAP_SERVERS = 'kafka:9092'
#BOOTSTRAP_SERVERS = 'localhost:9092'

def get_brand_channels(brand_id):
    '''
    fetch data from mysql table
    having mapping of brand and their channels
    '''
    channels = []
    try:
        if connection.is_connected():
            # Execute SELECT query
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM brand_channel_mapping where brand_id = {brand_id};")
            records = cursor.fetchall()

            # Print fetched records
            #import pdb;pdb.set_trace()
            for record in records:
                if record[2] == 1:
                    channels.append('email')
                if record[3] == 1:
                    channels.append('text')
                if record[4] == 1:
                    channels.append('whatsapp')
        
    except mysql.connector.Error as e:
        print(f"Error running database query: {e}")
    return channels

if __name__ == "__main__":
    try:
        #creating consumer
        consumer = KafkaConsumer(
            TOPIC_NOTIFICATION_IN,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            )
        
        #creating producer
        producer = KafkaProducer(bootstrap_servers=[BOOTSTRAP_SERVERS],
                         value_serializer=lambda x:json.dumps(x).encode("utf-8"))

        #creating mysql connection
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL database: {e}")

        #reading msg for topic "notification_handler"
        for task_msg in consumer:
            #import pdb; pdb.set_trace()
            task_msg = json.loads(task_msg.value)
            print(f'---------{task_msg}-----------------')
            if isinstance(task_msg, dict):
                tracking_id = task_msg['tracking_id']
                brand_id = task_msg['brand_id']
            
                channels = get_brand_channels(brand_id)
                #for each channel adding msg to respective topic
                for channel in channels:
                    print('-----writing in topic2------------')
                    producer.send(f"{channel}_notification", task_msg)
                    
            else:
                pass

        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    except Exception as e:
        print(e)

    