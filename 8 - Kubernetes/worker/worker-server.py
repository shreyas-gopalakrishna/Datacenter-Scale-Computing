#
# Worker server
#

import pika
import time
import subprocess
import redis
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from openalpr import Alpr
import socket
import io
import jsonpickle

# def findLicensePlate(img,filename):
#     img.save(filename)
#     result = subprocess.run(['alpr', filename], stdout=subprocess.PIPE)
#     data = result.stdout.decode('utf-8').split('\n')[1].split()
#     license, confidence = "", ""
#     if(len(data) > 1):
#         license, confidence = data[1], data[3]
#     else:
#         license, confidence = "Not found", "0"
#     return license, confidence

#
# Sample code from: https://gist.github.com/moshekaplan/5330395
#

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    deg_num, deg_denom = value[0]
    d = float(deg_num) / float(deg_denom)

    min_num, min_denom = value[1]
    m = float(min_num) / float(min_denom)

    sec_num, sec_denom = value[2]
    s = float(sec_num) / float(sec_denom)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data, debug=False):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = gps_info.get("GPSLatitude")
        gps_latitude_ref = gps_info.get('GPSLatitudeRef')
        gps_longitude = gps_info.get('GPSLongitude')
        gps_longitude_ref = gps_info.get('GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat *= -1

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon *= -1
    else:
        if debug:
            print("No EXIF data")

    return lat, lon

def getLatLon(image, debug=False):
    try:
        # image = Image.open(filename)
        exif_data = get_exif_data(image)
        return get_lat_lon(exif_data, debug)
    except:
        return None

def workerCallback(ch, method, properties, body):
    print(" [Y] Received %r" % "Data to Worker " + hostname + ":" + method.routing_key)
    data = jsonpickle.decode(body)
    # check geo tag, check LP, store in redis
    img = data['image']
    img_md5 = data['hash']
    filename = data['filename']
    ioBuffer = io.BytesIO(img)
    img = Image.open(ioBuffer)

    lat, lon = getLatLon(img)
    if(lat != None and lon != None):
        img.save(filename)
        results = alpr.recognize_file(filename)
        #print(results)
        if(results != None and len(results['results']) > 0):
            res = ''
            for i in range(0,len(results['results'][0]['candidates'])):
                res += 'License ' + str(results['results'][0]['candidates'][i]['plate']) + ' Confidence ' + str(results['results'][0]['candidates'][i]['confidence']) + " "
            channel.basic_publish(exchange='logs', routing_key='debug', body= hostname + ".worker.info " + "License Plate found! - " + res )
            license, confidence = str(results['results'][0]['plate']), str(results['results'][0]['confidence'])
            #print(license, confidence)
            encoded = license + ":" + confidence + ":" + str(lat) + ":" + str(lon)
            for i in range(1,len(results['results'])):
                license, confidence = results['results'][i]['plate'], results['results'][i]['confidence']
                encoded += "#" + license + ":" + confidence + ":" + lat + ":" + lon
            channel.basic_publish(exchange='logs', routing_key='debug', body= hostname + ".worker.info " + "License Plate found! - " + encoded)

            # adding to DB - 1
            if redisByChecksum.exists(img_md5):
                value = set(redisByChecksum.get(img_md5).decode('utf-8').split("#"))
            else:
                value = set()
            value.add(encoded)
            redisByChecksum.set(img_md5,"#".join(list(value)))
            channel.basic_publish(exchange='logs', routing_key='info', body= hostname + ".worker.info " + "Adding License Plate info to redisByChecksum ")

            # adding to DB - 2
            if(redisByName.exists(filename)):
                value = set(redisByName.get(filename).decode('utf-8').split("#"))
            else:
                value = set()
            value.add(img_md5)
            redisByName.set(filename,"#".join(list(value)))
            channel.basic_publish(exchange='logs', routing_key='info', body= hostname + ".worker.info " + "Adding Checksum info to redisByName ")

            # adding to DB - 3
            for entry in encoded.split("#"):
                license = entry.split(":")[0]
                if(redisMD5ByLicense.exists(license)):
                    value = set(redisMD5ByLicense.get(license).decode('utf-8').split("#"))
                else:
                    value = set()
                if(img_md5 in value):
                    channel.basic_publish(exchange='logs', routing_key='debug', body= hostname + ".worker.debug " + "Checksum already exits. Not adding to redisMD5ByLicense ")
                else:
                    value.add(img_md5)
                    redisMD5ByLicense.set(license,"#".join(list(value)))
                    channel.basic_publish(exchange='logs', routing_key='info', body= hostname + ".worker.info " + "Adding Checksum to redisMD5ByLicense ")
        else:
            channel.basic_publish(exchange='logs', routing_key='debug', body= hostname + ".worker.debug " + "No License Plate found!")
            print(" [x] No License Plate found!")
    else:
        print(" [x] Geo Tag doesn't exist!")
    #ch.basic_ack(delivery_tag=method.delivery_tag)

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

alpr = Alpr('us', '/etc/openalpr/openalpr.conf', '/usr/share/openalpr/runtime_data')

print(' [*] Waiting for messages. To exit press CTRL+C')


result = channel.queue_declare(queue='worker',durable=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange='toWorker', queue=queue_name, routing_key="toWorker")

channel.basic_consume(
    queue=queue_name, on_message_callback=workerCallback, auto_ack=True)

channel.start_consuming()