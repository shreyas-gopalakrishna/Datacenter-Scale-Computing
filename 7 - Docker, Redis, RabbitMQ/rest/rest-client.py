#
# You probably want to borrow code from your Lab6 solution to send the image
#
from __future__ import print_function
import requests
import json
import sys
import random


ip = '34.83.162.250'
addr = 'http://' + ip + ':5000'
image_url = addr + '/image/beetle.jpg'

headers = {'content-type': 'image/jpg'}
img = open('../images/beetle.jpg', 'rb').read()
# r = requests.put("http://somedomain.org/endpoint", data=payload)
response = requests.put(image_url, data=img, headers=headers)
responseJson = json.loads(response.text)
print(responseJson)

image_url = addr + '/image/car.jpg'

headers = {'content-type': 'image/jpg'}
img = open('../images/car.jpg', 'rb').read()
response = requests.put(image_url, data=img, headers=headers)
responseJson = json.loads(response.text)
print(responseJson)

image_url = addr + '/image/geotagged.jpg'

headers = {'content-type': 'image/jpg'}
img = open('../images/geotagged.jpg', 'rb').read()
response = requests.put(image_url, data=img, headers=headers)
responseJson = json.loads(response.text)
print(responseJson)

image_url = addr + '/image/plate1.png'

headers = {'content-type': 'image/png'}
img = open('../images/plate1.png', 'rb').read()
response = requests.put(image_url, data=img, headers=headers)
responseJson = json.loads(response.text)
print(responseJson)



image_url = addr + '/image/the-meat-car.jpg'

headers = {'content-type': 'image/jpg'}
img = open('../images/the-meat-car.jpg', 'rb').read()
response = requests.put(image_url, data=img, headers=headers)
responseJson = json.loads(response.text)
print(responseJson)
