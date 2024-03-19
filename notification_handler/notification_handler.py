from kafka import KafkaConsumer, KafkaProducer
import json

def get_brand_channels(brand_id):
    '''
    fetch data from mysql table
    having mapping of brand and their channels
    '''
    channel: list
    return channel

if __name__ == "__main__":
    try:
        consumer = KafkaConsumer(
            "email_notification",
            bootstrap_servers='192.168.0.10:9092',
            auto_offset_reset='earliest',
            group_id="notification-handler")
        
        producer = KafkaProducer(bootstrap_servers=['192.168.0.10:9092'],
                         value_serializer=lambda x:json.dumps(x).encode("utf-8"))
        print("starting the consumer")
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

    except Exception as e:
        print(e)