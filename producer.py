from azure.eventhub import EventHubProducerClient, EventData
import json
import time
import random
from faker import Faker

# --- CONFIGURATION ---
CONNECTION_STR = "Endpoint=sb://sentimentprojectrg.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_KEY_HERE"
EVENT_HUB_NAME = "user_reviews"

fake = Faker()

def generate_review():
    products = ["Laptop", "Headphones", "Smartphone", "SmartWatch", "Camera"]
    review_text = fake.sentence()
    
    # Simple hack to force some negative/positive sentiment
    if random.random() < 0.3:
        review_text = "Terrible! Broken and bad. I hate it."
    elif random.random() < 0.3:
        review_text = "Amazing! I love it. Best purchase ever."

    return {
        "review_id": str(fake.uuid4()),
        "user_id": random.randint(1000, 9999),
        "product_id": random.choice(products),
        "review_text": review_text,
        "timestamp": str(fake.date_time_this_year())
    }

def run_producer():
    print(f"🚀 Connecting to Azure Event Hub: {EVENT_HUB_NAME}...")
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR, 
        eventhub_name=EVENT_HUB_NAME
    )

    with producer:
        while True:
            batch = producer.create_batch()
            data = generate_review()
            json_data = json.dumps(data)
            
            # Add to batch
            batch.add(EventData(json_data))
            
            # Send batch
            producer.send_batch(batch)
            print(f"☁️ Sent to Cloud: {data['review_text'][:30]}...")
            time.sleep(2)

if __name__ == "__main__":
    run_producer()