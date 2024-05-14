import pika
import json
from faker import Faker
from models import Contact

fake = Faker()

# Підключення до RabbitMQ з використанням URL
rabbitmq_url = 'amqps://****************'  
params = pika.URLParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів
def generate_contacts(num):
    for _ in range(num):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            additional_info=fake.address()
        )
        contact.save()
        contact_id = str(contact.id)
        
        # Надсилання повідомлення у чергу
        message = json.dumps({'contact_id': contact_id})
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)
        print(f'Sent contact ID {contact_id}')

if __name__ == "__main__":
    generate_contacts(10)  # Генерація 10 фейкових контактів

# Закриття з'єднання
connection.close()
