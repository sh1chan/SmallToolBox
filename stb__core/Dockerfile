# XXX (ames0k0): Works on my machine
FROM ubuntu:24.04

RUN apt update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

WORKDIR /core

ADD . ./

RUN pip3 install --no-cache-dir --break-system-packages .