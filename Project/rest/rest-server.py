from flask import Flask, request, Response, send_from_directory

import jsonpickle
from PIL import Image
import io
import hashlib
import pika
import sys
import json
import socket
import redis
import os

from google.cloud import storage

# MySQL library
import mysql.connector
from mysql.connector import Error

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/DCSC.json"

# Initialize the Flask application
# app = Flask(__name__)
app = Flask(__name__)


bucket_name = 'dcsc-3-bucket'

db_host = '34.82.191.254'
db_name = 'dcsc'
db_user = 'root'
db_password = 'csci5253'

try:
   connectionDB = mysql.connector.connect(host=db_host,
                                        database=db_name,
                                        user=db_user,
                                        password=db_password)
except mysql.connector.Error as error:
    print("Error Connecting to MySQL DB {}".format(error))

redisAuthentication = redis.Redis(host='redis', db=1)
redisDocumentsByUser = redis.Redis(host='redis', db=2)
redisDocumentsByKeyword = redis.Redis(host='redis', db=3)

connection = pika.BlockingConnection(
pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='toWorker', exchange_type='direct')

channel.basic_qos(prefetch_count=1)

hostname = socket.gethostname()
debug = hostname+".debug"
info = hostname+".info"

# route http posts to this method
@app.route('/signUp', methods=['POST'])
def signUp():
    r = request.form
    # use the username to get password associated with user.
    try:
        username = r.get('username')
        password = r.get('password')
        response = dict()
        response["username"] = username
        print(username,password)
        if redisAuthentication.exists(username):
            passwordFromDatabase = redisAuthentication.get(username).decode('utf-8')
            response["password"] = passwordFromDatabase
            response["message"] = "User Already Exists!"
        else:
            print(username,password,"123")
            redisAuthentication.set(username,password)
            response["password"] = password
            response["authentication"] = "User Created!"
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response_pickled, 401, {'WWW-Authenticate':'Basic realm="Login Required"'})


# route http posts to this method
@app.route('/auth', methods=['POST'])
def authenticate():
    r = request.form
    # use the username to get password associated with user.
    try:
        username = r.get('username')
        password = r.get('password')
        response = dict()
        response["username"] = username
        if redisAuthentication.exists(username):
            passwordFromDatabase = redisAuthentication.get(username).decode('utf-8')
            if(password == passwordFromDatabase):
                response["authentication"] = "success"
                response_pickled = jsonpickle.encode(response)
                return Response(response=response_pickled, status=200, mimetype="application/json")
            else:
                response["authentication"] = "failure"
        else:
            response["authentication"] = "User does not exist"
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response_pickled, 401, {'WWW-Authenticate':'Basic realm="Login Required"'})

# route http posts to this method
@app.route('/user', methods=['POST'])
def documents():
    r = request.form
    print(r)
    # use the username to get documents associated with user.
    try:
        username = r.get('username')
        print(username)
        response = dict()
        response["username"] = username
        if redisDocumentsByUser.exists(username):
            print(json.loads(redisDocumentsByUser.get(username).decode('utf-8')))
            listOfDocuments = json.loads(redisDocumentsByUser.get(username).decode('utf-8'))
            print(listOfDocuments)
            response["documents"] = listOfDocuments
        else:
            response["documents"] = None
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route('/keywords', methods=['POST'])
def keywords():
    r = request.form
    # use the keyword to get documents associated with keyword.
    try:
        username = r.get('username')
        keywords = r.get('keywords').split(',')
        response = dict()
        response["username"] = username
        response["keywords"] = keywords
        if redisDocumentsByUser.exists(username):
            listOfDocuments = list() #matches for documents

            listOfDocumentsForUser = json.loads(redisDocumentsByUser.get(username).decode('utf-8'))
            print(listOfDocumentsForUser,"user\n\n\n\n\n")
            listOfDocumentsIdForUser = [x['documentId'] for x in listOfDocumentsForUser]
            print(listOfDocumentsIdForUser,"usernext \n\n\n\n")
            listOfDocumentsIdForUserProcessed = list()

            # find all documents with each keyword
            for keyword in keywords:
                print(keyword,"\n")
                if redisDocumentsByKeyword.exists(keyword):
                    listOfDocumentsForKeyword = json.loads(redisDocumentsByKeyword.get(keyword).decode('utf-8'))
                    print(listOfDocumentsForKeyword,"keyword \n")
                    for keyDocument in listOfDocumentsForKeyword:
                        if keyDocument in listOfDocumentsIdForUser and not keyDocument in listOfDocumentsIdForUserProcessed:
                            listOfDocuments.append(keyDocument)
                            listOfDocumentsIdForUserProcessed.append(keyDocument)
            response["documents"] = listOfDocuments
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route('/document/<documentId>', methods=['POST'])
def document(documentId):
    r = request.form
    # use the keyword to get documents associated with keyword.
    try:
        username = r.get('username')
        response = dict()
        response["username"] = username
        response["documentId"] = documentId
        # get the content for the document from SQL

        try:
            cursor = connectionDB.cursor()
            sql_fetch_blob_query = """SELECT * from text_in_document where username = %s and documentId = %s"""

            get_blob_tuple = (username,documentId,)
            cursor.execute(sql_fetch_blob_query, get_blob_tuple)
            record = cursor.fetchall()

            if (len(record) > 1):
                print("There are more than one record (%d) for %s, %r" %
                        (len(record), username, record))
            else:
                print("record for %s, %r" % (username, record))
            for row in record:
                print("username = %s, documentId = %s, content= %s" % (row[0], row[1], row[2]))
                content = row[2] 
        except mysql.connector.Error as error:
            print("Failed to read BLOB data from MySQL table {}".format(error))
        finally:
            cursor.close()
        
        response["documentContent"] = content
    except:
        response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# function to upload image/document into Google Cloud Storage bucket. - from bytes
def upload_blob_bytes(bucket_name, source_bytes, destination_blob_name, ext):
    """Uploads a file to the bucket."""
    if(ext == 'jpg' or ext == 'jpeg' or ext == 'png'):
        ext = 'image/jpeg'
    elif(ext == 'pdf'):
        ext = 'application/pdf'
    else:
        ext = 'text/plain'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # blob.upload_from_file(file_obj=source_bytes, size=len(source_bytes))
    blob.upload_from_string(source_bytes, content_type=ext)

    print('Data {} uploaded to {}.'.format(
        'source_bytes',
        destination_blob_name))

# function to upload image/document into Google Cloud Storage bucket. - from filename
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    print(storage_client)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    print(blob)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


# route http posts to this method
@app.route('/upload/<filename>', methods=['POST'])
def upload(filename):
    ext = filename.split('.')[-1]
    r = request.form
    print(request.form,"rrrr")
    print(request.files)
    f = request.files['file'].read()
    #print(f)
    print(request.form.get('filename'))
    # convert the data to a PIL image type so we can extract dimensions
    if(1==1):#try:
        username = r.get('username')
        fileDescription = r.get('fileDescription')
        md5 = hashlib.md5()
        md5.update(f)
        img_md5 = md5.hexdigest()
        data = dict()
        data['documentId'] = img_md5
        data['filename'] = filename
        data['username'] = username
        data['fileDescription'] = fileDescription
        print(data)

        # store file in google bucket.
        upload_blob_bytes(bucket_name, f, img_md5, ext)

        # send file detials to worker via rabbitmq.
        channel.basic_publish(
            exchange='toWorker',
            routing_key='toWorker',
            body=jsonpickle.encode(data))
        print(" [x] Sent %r" % filename)
        data['status'] = 'success'
        # build a response dict to send back to client
        response = data
    #except:
    #    response = { 'error' : 'Could not process'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


app.run(host="0.0.0.0", port=5000)

#connection.close()
