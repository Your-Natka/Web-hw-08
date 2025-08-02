# pylint: disable=no-member

import pika
import json
from mongoengine import connect
from db.models import Contact

connect(db="contacts_db", host="mongodb://localhost:27017/contacts_db", alias="default")

def send_sms_stub(contact: Contact):
    print(f"📲 Надсилаємо SMS до {contact.phone}...")
    contact.is_sent = True
    contact.save()

def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data["id"]).first()
    if contact and contact.send_method == "sms" and not contact.is_sent:
        send_sms_stub(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="sms_queue")
channel.basic_consume(queue="sms_queue", on_message_callback=callback)

try:
    print("📥 Очікуємо SMS-повідомлення...")
    channel.start_consuming()
except KeyboardInterrupt:
    print("🛑 Зупинено вручну. Вихід...")
    channel.stop_consuming()
    connection.close()
