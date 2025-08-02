# pylint: disable=no-member

import pika
import json
from mongoengine import connect
from db.models import Contact

connect(db="contacts_db", host="mongodb://localhost:27017/contacts_db", alias="default")

def send_email_stub(contact: Contact):
    print(f"📧 Надсилаємо email до {contact.email}...")
    contact.is_sent = True
    contact.save()

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        contact = Contact.objects(id=data["id"]).first()
        if contact and contact.send_method == "email" and not contact.is_sent:
            send_email_stub(contact)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"❌ Помилка під час обробки повідомлення: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="email_queue")
channel.basic_consume(queue="email_queue", on_message_callback=callback)

print("📥 Очікуємо email-повідомлення...")
channel.start_consuming()
