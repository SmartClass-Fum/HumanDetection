FROM python:3.8.11-slim-buster
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install -y python3-pip
WORKDIR person_detector
COPY . .
RUN pip3 install -r requirements.txt
RUN python3 download_models.py
WORKDIR detector/YOLOv3/nms
RUN chmod -x build.sh
RUN build.sh
WORKDIR ../../..



