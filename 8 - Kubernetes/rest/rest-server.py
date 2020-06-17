##
## Sample Flask REST server implementing two methods
##
from flask import Flask, request, Response
import jsonpickle
import numpy as np
from PIL import Image
import io
import hashlib
import pika
import sys
import json
import socket
import redis

# Initialize the Flask application
app = Flask(__name__)

connection = pika.BlockingConnection(
pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='toWorker', exchange_type='direct')
channel.exchange_declare(exchange='logs', exchange_type='topic')

channel.basic_qos(prefetch_count=1)

hostname = socket.gethostname()
debug = hostname+".debug"
info = hostname+".info"

redisByChecksum = redis.Redis(host='redis', db=1)
redisByName = redis.Redis(host='redis', db=2)
redisMD5ByLicense = redis.Redis(host='redis', db=3)

# route http posts to this method
@app.route('/image/<filename>', methods=['PUT'])
def image(filename):
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        # print(filename)
        channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Received "+ filename)
        md5 = hashlib.md5()
        md5.update(r.data)
        img_md5 = md5.hexdigest()
        # ioBuffer = io.BytesIO(r.data)
        # img = Image.open(ioBuffer)
        data = dict()
        data['hash'] = img_md5
        data['image'] = r.data
        data['filename'] = filename
        # debug message
        channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Sending "+ filename + " to Worker")
        # pass md5 and image to worker
        channel.basic_publish(
            exchange='toWorker',
            routing_key='toWorker',
            body=jsonpickle.encode(data))
        print(" [x] Sent %r" % img_md5)
        # build a response dict to send back to client
        response = {
            'hash': img_md5,
            }
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/hash/<checksum>', methods=['GET'])
def hash(checksum):
    try:
        r = request
        channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Getting info for checksum - " + checksum)
        response = dict()
        # check in db
        if redisByChecksum.exists(checksum):
            value = redisByChecksum.get(checksum).decode('utf-8')
            channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Checksum info found "+ value)
            response["output"] = value.split("#")
        else:
            response["output"] = "Checksum info does not exist! "
            channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Checksum info not found")
    except:
        response = { 'error' : 'Could not process'}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/license/<licensePlate>', methods=['GET'])
def license(licensePlate):
    try:
        r = request
        channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "Getting info for licensePlate - " + licensePlate)
        response = dict()
        print(licensePlate)
        # check in db
        if redisMD5ByLicense.exists(licensePlate):
            value = redisMD5ByLicense.get(licensePlate).decode('utf-8')
            print(value)
            channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "License Plate info found "+ value)
            response["output"] = value.split("#")
        else:
            response["output"] = "LicensePlatem info does not exist! "
            channel.basic_publish(exchange='logs', routing_key='debug', body="REST - " + "License Plate info not found")
    except Exception as e:
        print(e)
        response = { 'error' : 'Could not process'}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)

#connection.close()