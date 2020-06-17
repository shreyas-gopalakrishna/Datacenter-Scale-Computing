import pika
import redis
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import socket
import io
import jsonpickle
import json
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/DCSC.json"

# MySQL library
import mysql.connector
from mysql.connector import Error

from google.cloud import storage
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud import vision_v1
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import io

# function to download image/document into Google Cloud Storage bucket. - from bytes
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def download_blob_bytes(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    bytes_data = blob.download_as_string()

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        'blob bytes data'))

    return bytes_data

def vision(fileBytes):
    # check if file or document and then perform OCR on it.
    image = vision_v1.types.Image(content=fileBytes)

    response = client.document_text_detection(image=image)

    blockText = ''

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print('\nBlock confidence: {}\n'.format(block.confidence))
            blockText = ''

            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(
                #     paragraph.confidence))
                paragraphText = ''
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    paragraphText += word_text + " "
                    # print('Word text: {} (confidence: {})'.format(
                    #     word_text, word.confidence))

                    # for symbol in word.symbols:
                    #     print('\tSymbol: {} (confidence: {})'.format(
                    #         symbol.text, symbol.confidence))
                paragraphText += '\n'
                blockText += paragraphText
        print(blockText)
    return blockText

def storeContentInSql(username, documentId, textFromDocument):
    try:
        cursor = connectionDB.cursor()
        sql_insert_blob_query = """ INSERT INTO text_in_document
                          (username, documentId, content) VALUES (%s, %s, %s)"""

        insert_text_tuple = (username, documentId, textFromDocument)
        result = cursor.execute(sql_insert_blob_query, insert_text_tuple)
        connectionDB.commit()
        print(username, documentId, textFromDocument)
    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
    finally:
        cursor.close()

def nlpClassifyText(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    response = client.classify_text(document)
    categoriesList = list()
    # Loop through classified categories returned from the API
    for category in response.categories:
        categoryDict = dict()
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print(u"Category name: {}".format(category.name))
        categoryDict['name'] = category.name
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        print(u"Confidence: {}".format(category.confidence))
        categoryDict['confidence'] = category.confidence
        categoriesList.append(categoryDict)
    return categoriesList

def formatText(text):
    text = text.lower()
    text = text.replace("\n"," ").replace(".","").replace(",","")
    # text = text.replace(" the "," ").replace(" of ","").replace(" a ","").replace(" at ","").replace(" that ","")
    return text


def workerCallback(ch, method, properties, body):
    print(" [Y] Received %r" % "Data to Worker " + hostname + ":" + method.routing_key)
    data = jsonpickle.decode(body)
    print(data) # data will contain document/image id, filename and username

    # get the file from bucket
    fileFromBucket = download_blob_bytes(bucket_name, data['documentId'])

    # perform OCR on the file and store results in SQL
    textFromDocument = vision(fileFromBucket)

    storeContentInSql(data['username'], data['documentId'], textFromDocument)

    # Classify the text obtained from document and store results

    categories = nlpClassifyText(textFromDocument)

    document = dict()
    document['documentId'] = data['documentId']
    document['filename'] = data['filename']
    document['fileDescription'] = data['fileDescription']
    document['categories'] = categories

    print(document,data['username'])

    if redisDocumentsByUser.exists(data['username']):
        listOfDocuments = json.loads(redisDocumentsByUser.get(data['username']).decode('utf-8'))
        if not data['documentId'] in [ doc['documentId'] for doc in listOfDocuments]:
            listOfDocuments.append(document)
            redisDocumentsByUser.set(data['username'],json.dumps(listOfDocuments))
        else:
            pass #document already exists
    else:
        redisDocumentsByUser.set(data['username'],json.dumps([document]))
    
    # store keywords
    formattedTextFromDocument = formatText(textFromDocument)

    for word in formattedTextFromDocument.split(' '):
        if( len(word) > 3 and redisDocumentsByKeyword.exists(word)):
            listOfDocumentsId = json.loads(redisDocumentsByKeyword.get(word).decode('utf-8'))
            if not data['documentId'] in listOfDocumentsId:
                listOfDocumentsId.append(data['documentId'])
                redisDocumentsByKeyword.set(word,json.dumps(listOfDocumentsId))
            else:
                pass
        else:
            if(len(word) > 3):
                redisDocumentsByKeyword.set(word,json.dumps([data['documentId']]))
    #ch.basic_ack(delivery_tag=method.delivery_tag)


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

client = ImageAnnotatorClient()

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


print(' [*] Waiting for messages. To exit press CTRL+C')

result = channel.queue_declare(queue='worker',durable=True)
queue_name = result.method.queue

channel.queue_bind(
        exchange='toWorker', queue=queue_name, routing_key="toWorker")

channel.basic_consume(
    queue=queue_name, on_message_callback=workerCallback, auto_ack=True)

channel.start_consuming()
