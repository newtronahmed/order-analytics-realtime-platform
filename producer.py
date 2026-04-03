import time
import json
from kafka import KafkaProducer

# Initialize Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Function to generate order events
def generate_order_event(order_id, customer_id, product_id, quantity):
    event = {
        'order_id': order_id,
        'customer_id': customer_id,
        'product_id': product_id,
        'quantity': quantity,
        'timestamp': time.time()
    }
    return event

# Main loop to produce order events
if __name__ == '__main__':
    try:
        for i in range(10):  # Generate 10 events
            order_event = generate_order_event(i, f'cust_{i}', f'prod_{i}', i + 1)
            producer.send('orders', order_event)
            print(f'Produced order event: {order_event}')
            time.sleep(1)  # Sleep for a second between events
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()