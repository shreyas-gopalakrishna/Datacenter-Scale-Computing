import grpc
from concurrent import futures
import time
import io
import numpy as np
from PIL import Image

# import the generated classes
import grpc_protocol_pb2
import grpc_protocol_pb2_grpc

class CalculateSumServicer(grpc_protocol_pb2_grpc.CalculateSumServicer):
    def Add(self, request, context):
        return  grpc_protocol_pb2.Answer(sum=int(request.x+request.y))

    def ImageWH(self, request, context):
        ioBuffer = io.BytesIO(request.img)
        img = Image.open(ioBuffer)
        return grpc_protocol_pb2.Size(width=img.size[0],height = img.size[1])

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

grpc_protocol_pb2_grpc.add_CalculateSumServicer_to_server(
    CalculateSumServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
# since server.start() will not block,
# a sleep-loop is added to keep alive
#try:
#    while True:
#        time.sleep(86400)
#except KeyboardInterrupt:
#    server.stop(0)

