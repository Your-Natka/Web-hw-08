# pylint: disable=no-member

import pika
import json
import time
import traceback
from mongoengine import connect
from db.models import Contact
from bson import ObjectId

connect(db="contacts_db", host="mongodb://host.docker.internal:27017/contacts_db", alias="default")

def send_email_stub(contact: Contact):
    print(f"📧 Надсилаємо email до {contact.email}...")
    contact.is_sent = True
    contact.save()

def callback(ch, method, _, body):
    try:
        data = json.loads(body)
        contact = Contact.objects(id=ObjectId(data["id"])).first()
        if contact and contact.send_method == "email" and not contact.is_sent:
            send_email_stub(contact)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ Помилка під час обробки повідомлення: {e}")
        traceback.print_exc()
        ch.basic_nack(delivery_tag=method.delivery_tag)

for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
        break
    except pika.exceptions.AMQPConnectionError:
        print("⏳ Очікуємо RabbitMQ...")
        time.sleep(5)
else:
    print("❌ RabbitMQ недоступний. Завершення.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="email_queue")
channel.basic_consume(queue="email_queue", on_message_callback=callback)

print("📥 Очікуємо email-повідомлення...")
channel.start_consuming()
