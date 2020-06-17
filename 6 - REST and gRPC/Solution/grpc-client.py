from __future__ import print_function
import requests
import json
from time import perf_counter
import sys
import random
import grpc
# generated classes
import grpc_protocol_pb2
import grpc_protocol_pb2_grpc

def usage():
    print("python grpc-client.py localhost add 1000")
    print("python grpc-client.py localhost image 1000")

def add(addr, iterations):
    channel = grpc.insecure_channel(addr)
    # create a stub (client)
    stub = grpc_protocol_pb2_grpc.CalculateSumStub(channel)
    start = perf_counter()
    num1 = random.randint(0, 1000)
    num2 = random.randint(0, 1000)
    for i in range(0, iterations):
        # create a valid request message
        number = grpc_protocol_pb2.Numbers(x=num1, y=num2)
        response = stub.Add(number)
        # if(response.sum == num1+num2):
        #    print("correct")
        # else:
        #    print("incorrect")
    stop = perf_counter()
    print("Average Time taken ADD - " + str((stop-start)/iterations))

def image(addr, iterations):
    channel = grpc.insecure_channel(addr)
    stub = grpc_protocol_pb2_grpc.CalculateSumStub(channel)
    # create a valid request message
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    image = grpc_protocol_pb2.Image(img=img)
    start = perf_counter()
    for i in range(0, iterations):
        response = stub.ImageWH(image)
        print(response.width,response.height)
    stop = perf_counter()
    print("Average Time taken IMAGE - " + str((stop-start)/iterations))

if(len(sys.argv) == 4):
    addr = sys.argv[1] + ':50051'
    iterations = int(sys.argv[3])
    action = sys.argv[2]
    if(action == "add"):
        add(addr,iterations)
    elif(action == "image"):
        image(addr,iterations)
else:
    usage()

