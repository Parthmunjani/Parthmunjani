import pika
import uuid
import json

credentials = pika.PlainCredentials(username='guest', password='guest', erase_on_connect=True)
parameters = pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=credentials)

uuid_value = str(uuid.uuid4())

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

json_data = {
    'uuid': uuid_value
}

message = json.dumps(json_data)

properties = pika.BasicProperties(
    message_id=uuid_value
)

channel.basic_publish(exchange='', routing_key='hello', body=message, properties=properties)
print(f" [x] Sent UUID: {uuid_value}")

connection.close()
