## CSCI 5253 - Data Center Scale Computing - Lab 6

### Part 1 - REST
This section is added with a new GET call to the server to add 2 integers. The REST API  `/add/X/Y` is being used to retrieve numbers and add them.
Random numbers were generated from the client and 1000 requests were sent to add them. The API `/image` was used to get the width and height of an image using POST. 

Command to run server: `python3 rest-server.py`
Command to run client: `python3 rest-client.py <ip> add 1000`
Command to run client: `python3 rest-client.py <ip> image 1000`

### Part 2 - gRPC
The protocol buffer was set up to take in numbers and images as a message. And service is defined which takes in numbers - adds them and takes in images and finds its width and height.

Used the command `python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc-protocol.proto` to generate gRPC classes.

Command to run server: `python3 grpc-server.py`
Command to run server: `python3 grpc-client.py <ip> add 1000`
Command to run server: `python3 grpc-client.py <ip> image 1000`


Both REST and gRPC was tested in VM instances created using snapshot in the same zone and different zones ( `us-west1-b` and `europe-west3-a`) and their average time for each method were recorded.
Command to create these instances using snapshot in same and different zone: `python create_snapshot.py`

### Statistics

The data represents average time in milliseconds 

| METHOD  | Local  | Same-Zone | Different Region |
| :------------ |:---------------:| -----:|-----:|
| REST add | 2.5 |2.67 |281.21 |
| REST img | 4.5  |10.20 |1144.24|
| gRPC add | 0.45 |0.54 |138.02|
| gRPC img | 6.05 |7.82 |176.82|
| PING     | 0.045|0.375|136.850|

### Takeaway
- The add service provided consumes less time compared to the image service since image service involved transferring the image which consumes more bandwidth.
- The gRPC mechanism is found to be must faster compared to the REST API. For both the services (add and image) the gRPC on an average is 5-6 times faster than REST.
- gRPC was found to be faster since it uses protocol buffers whereas REST used JSON.
- The speed can also be since gRPC uses HTTP/2 and single TCP connection whereas REST uses HTTP 1.1 and new TCP connection for every request.
- The test took a longer time for the same services and methods when communication happens across different regions compared to the same zone which was verified using the methods as well as the ping command.

### Sources
- https://grpc.io/docs/tutorials/basic/python/
- https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/

*-Shreyas Gopalakrishna*
