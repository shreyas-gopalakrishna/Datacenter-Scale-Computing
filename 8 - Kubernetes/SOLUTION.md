## CSCI 5253 - Data Center Scale Computing - Lab 8

Open Alpr - Kubernetes

### Solution
My solution is implemented using docker containers, which are managed by kubernetes. 
Redis handles the storage, RabbitMQ handles the message passing to workers REST handles getting images Workers use the ALPR service to get Liscence plate info and store in Redis.

### Steps to Run code
1. `sh redis-launch.sh` creates docker image of redis, pushes it to kubernetes, and exposes port.
2. `sh rabbitmq-launch.sh` creates docker image of rabbitmq, pushes it to kubernetes, and exposes port.
3. `sh rest-launch.sh` creates docker image with flask and other modules installed, pushes it to kubernetes, and exposes 5000 port for REST API.
4. `sh worker-launch.sh` creates docker image of worker with open alpr installed with other modules and pushes it to kubernetes.
5. `python3 rest-client.py` sends images to test the service.


*-Shreyas Gopalakrishna*

