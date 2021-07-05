FROM python:3.8.11-slim-buster
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get -y update 
RUN apt-get -y upgrade
RUN apt install -y software-properties-common
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
WORKDIR person_detector
COPY . .
RUN pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirements.txt
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN python3 download_models.py
WORKDIR detector/YOLOv3/nms/ext
RUN python3 build.py build_ext develop
WORKDIR ../../../..
ENTRYPOINT [ "python3", "main.py" ]