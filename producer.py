# pylint: disable=no-member

import pika
import json
from faker import Faker
from mongoengine import connect
from db.models import Contact

connect(db="contacts_db", host="mongodb://localhost:27017/contacts_db", alias="default")

fake = Faker()

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Створюємо черги
channel.queue_declare(queue="email_queue")
channel.queue_declare(queue="sms_queue")

# Генеруємо контакти
for _ in range(10):
    method = fake.random_element(["email", "sms"])
    contact = Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        send_method=method
    ).save()

    message = json.dumps({"id": str(contact.id)})
    queue_name = "email_queue" if method == "email" else "sms_queue"
    channel.basic_publish(exchange="", routing_key=queue_name, body=message)
    print(f"📤 Відправлено контакт {contact.fullname} у чергу {queue_name}")

connection.close()
