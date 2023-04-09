FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip 
RUN pip3 install --upgrade Pillow
RUN pip3 install networkx
RUN pip3 install matplotlib
WORKDIR /usr/local/bin/
COPY Iot.py .
CMD python3 Iot.py