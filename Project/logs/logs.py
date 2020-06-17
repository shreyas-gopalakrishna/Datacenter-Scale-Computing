#!/usr/bin/env python
import pika
import sys
import socket


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='topic')

channel.basic_qos(prefetch_count=1)

hostname = socket.gethostname()

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange='logs', queue=queue_name, routing_key='debug')

channel.queue_bind(
        exchange='logs', queue=queue_name, routing_key='info')

print(' [*] Waiting for logs. To exit press CTRL+C')


def logCallback(ch, method, properties, body):
    #print(" [x] Received %r %r " % (hostname + ":" + method.routing_key, body))
    if(method.routing_key == 'debug'):
        print(" [x] Received Debug - %r " % (body.decode('utf-8')))
    if(method.routing_key == 'info'):
        print(" [x] Received Info - %r " % (body.decode('utf-8')))
    print()
    #ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name, on_message_callback=logCallback, auto_ack=True)

channel.start_consuming()