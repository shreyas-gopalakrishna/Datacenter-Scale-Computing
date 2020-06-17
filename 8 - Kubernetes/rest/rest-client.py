# from __future__ import print_function
# import requests
# import json
# import time
# import sys, os

# def doImage(addr, filename, debug=False):
    # # prepare headers for http request
    # headers = {'content-type': 'image/png'}
    # img = open(filename, 'rb').read()
    # # send http request with image and receive response
    # image_url = addr + '/image' + "/" + os.path.basename(filename)
    # response = requests.post(image_url, data=img, headers=headers)
    # if debug:
        # # decode response
        # print("Response is", response)
        # print(json.loads(response.text))

# host = sys.argv[1]
# cmd = sys.argv[2]

# addr = 'http://{}:5000'.format(host)

# if cmd == 'image':
    # filename = sys.argv[3]
    # reps = int(sys.argv[4])
    # start = time.perf_counter()
    # for x in range(reps):
        # doImage(addr, filename, True)
    # delta = ((time.perf_counter() - start)/reps)*1000
    # print("Took", delta, "ms per operation")
# elif cmd == 'add':
    # reps = int(sys.argv[3])
    # start = time.perf_counter()
    # for x in range(reps):
        # doAdd(addr)
    # delta = ((time.perf_counter() - start)/reps)*1000
    # print("Took", delta, "ms per operation")
# else:
    # print("Unknown option", cmd)

from __future__ import print_function
import requests
import json
import sys
import random


def usage():
    print("rest-client.py [ip] image [img] 1")

def image(addr, img_name):
    image_url = addr + '/image/' + img_name[10:]
    print(image_url)
    headers = {'content-type': 'image/jpg'}
    img = open(img_name, 'rb').read()
    response = requests.put(image_url, data=img, headers=headers)
    responseJson = json.loads(response.text)
    print(responseJson)

if(len(sys.argv) == 5):
    addr = 'http://' + sys.argv[1] + ':5000'
    img_name = sys.argv[3]
    image(addr,img_name)
else:
    usage()