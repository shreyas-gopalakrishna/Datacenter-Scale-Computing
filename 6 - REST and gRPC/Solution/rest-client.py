from __future__ import print_function
import requests
import json
from time import perf_counter
import sys
import random


def usage():
    print("python rest-client.py localhost add 1000")
    print("python rest-client.py localhost image 1000")

def add(addr, iterations):
    start = perf_counter()
    for i in range(0, iterations):
        num1 = random.randint(0, 1000)
        num2 = random.randint(0, 1000)
        URL = addr + '/api/add/' + str(num1) + '/' + str(num2)
        response = requests.get(url = URL)
        # decode response
        responseJson = json.loads(response.text)
        # print(responseJson)
        #if(responseJson["sum"] == num1+num2):
        #    print("correct")
        #else:
        #    print("incorrect")
    stop = perf_counter()
    print("Average Time taken ADD - " + str((stop-start)/iterations))

def image(addr, iterations):
    # prepare headers for http request
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    # send http request with image and receive response
    image_url = addr + '/api/image'
    start = perf_counter()
    for i in range(0, iterations):
        response = requests.post(image_url, data=img, headers=headers)
        # decode response
        #print("Response is", response)
        responseJson = json.loads(response.text)
    stop = perf_counter()
    print("Average Time taken IMAGE - " + str((stop-start)/iterations))

if(len(sys.argv) == 4):
    addr = 'http://' + sys.argv[1] + ':5000'
    iterations = int(sys.argv[3])
    action = sys.argv[2]
    if(action == "add"):
        add(addr,iterations)
    elif(action == "image"):
        image(addr,iterations)
else:
    usage()