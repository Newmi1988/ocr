FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip
RUN apt update && apt install -y libsm6 libxext6
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get -y install tesseract-ocr
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt