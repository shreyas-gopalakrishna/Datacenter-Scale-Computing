FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip git

RUN pip3 install --upgrade pika
RUN pip3 install jsonpickle
RUN pip3 install pillow
RUN pip3 install numpy
RUN pip3 install redis

COPY logs.py .
CMD ["python3", "logs.py"]