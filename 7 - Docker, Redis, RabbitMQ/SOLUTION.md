## CSCI 5253 - Data Center Scale Computing - Lab 7

API to take image and provide Liscence plate recognision using Open ALPR

### Task Completed
-  Created API to take image and provide Liscence plate recognision.

### Solution
Redis handles the storage
RabbitMQ handles the message passing to workers
REST handles getting images 
Workers use the ALPR service to get Liscence plate info and store in Redis.

### Steps to Run code
1. `sh redis-launch.sh` creates instance, installs redis and runs redis.
2. `sh rabbitmq-launch.sh` creates instance, installs rabbitmq and runs rabbitmq.
3. `sh rest-launch.sh` creates instance and starts REST server.
4. `sh worker-launch.sh` creates a worker and installs necessary modules.
5. `sh worker-addworker.sh` adds new workers using image.
6. `python3 rest-client.py` sends images to test the service.



*-Shreyas Gopalakrishna*

