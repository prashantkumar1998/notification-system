from kafka import KafkaConsumer, KafkaProducer
import json
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_brand_channels(brand_id):
    '''
    fetch data from mysql table
    having mapping of brand and their channels
    '''
    try:
        if connection.is_connected():
            # Execute SELECT query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM brand_channel_mapping;")
            records = cursor.fetchall()

            # Print fetched records
            channels = []
            for record in records:
                if record[0] == 1:
                    channels.append('email')
                if record[1] == 1:
                    channels.append('text')
                if record[2] == 1:
                    channel.append('whatsapp')
        
    except mysql.connector.Error as e:
        print(f"Error running database query: {e}")

    return channels

if __name__ == "__main__":
    try:
        #creating consumer
        consumer = KafkaConsumer(
            "notification-handler",
            bootstrap_servers='kafka:9092',
            auto_offset_reset='earliest',
            group_id="notification-handler-group")
        
        #creating producer
        producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
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

        #reading msg for topic "email_notification"
        for task_msg in consumer:
            task_msg = json.loads(task_msg.value)
            tracking_id = task_msg['tracking_id']
            brand = task_msg['brand']
            kafka_push_msg = {
                "tracking_id":tracking_id,
                "brand": brand
            }
            channels = get_brand_channels()
            for channel in channels:
                producer.send(f"{channel}_notification", kafka_push_msg)

        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    except Exception as e:
        print(e)

    