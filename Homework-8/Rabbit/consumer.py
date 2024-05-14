import pika
import json
from models import Contact

# Підключення до RabbitMQ з використанням URL
rabbitmq_url = 'amqps://****************'
params = pika.URLParameters(rabbitmq_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Імітація функції надсилання повідомлення
def send_email(contact):
    print(f"Sending email to {contact.email}")
    # Функція-заглушка
    return True

# Обробка повідомлень
def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    
    if contact and not contact.message_sent:
        if send_email(contact):
            contact.message_sent = True
            contact.save()
            print(f"Message sent to {contact.email}")

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
