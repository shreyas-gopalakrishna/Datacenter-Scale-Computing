#!/bin/sh
#
# This is the script you need to provide to launch a rest instance
#

cat > Dockerfile <<EOF
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip git
RUN git clone https://github.com/pallets/flask.git
RUN cd flask/examples/tutorial
COPY setup.py .
COPY README.rst .
RUN python3 setup.py install
RUN pip3 install -e .

RUN pip3 install --upgrade pika
RUN pip3 install jsonpickle
RUN pip3 install pillow
RUN pip3 install numpy
RUN pip3 install redis

COPY rest-server.py .
COPY log.py .

CMD ["python3", "rest-server.py"]
EOF

docker build -t rest:0.1 .

docker tag rest:0.1 gcr.io/dcsc-2/rest:0.1
docker push gcr.io/dcsc-2/rest:0.1

kubectl create deployment rest --image=gcr.io/dcsc-2/rest:0.1
kubectl expose deployment rest --type=LoadBalancer --port 5000
