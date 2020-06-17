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
RUN pip3 install google-cloud-storage
RUN pip3 install mysql-connector-python
RUN pip3 install --upgrade google-cloud-language
RUN pip3 install --upgrade google-cloud-vision

COPY rest-server.py .
COPY DCSC.json .
CMD ["ENV" ,"PYTHONUNBUFFERED=0"]
CMD ["export","GOOGLE_APPLICATION_CREDENTIALS='./DCSC.json'"]
CMD ["python3", "rest-server.py"]