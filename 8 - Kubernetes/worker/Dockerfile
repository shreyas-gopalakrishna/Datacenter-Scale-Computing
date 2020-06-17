FROM ubuntu:eoan

WORKDIR /srv
COPY worker.py /srv
RUN apt-get update
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y openalpr
RUN (cd /usr/share/openalpr/runtime_data/ocr/; cp tessdata/lus.traineddata .)
RUN apt-get install -y python3 python3-pip python3-pillow python3-openalpr python3-redis
RUN pip3 install --upgrade pika
RUN pip3 install numpy
RUN pip3 install jsonpickle
RUN pip3 install pillow
RUN pip3 install redis
RUN cd /srv

# Run rest-server using python3 when the container launches
CMD ["python3", "worker.py"]