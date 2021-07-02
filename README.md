# Human Detector  for SmartClass


## Installaion using  pip
Install all dependencies 
```bash
pip install -r requirements.txt
```

Compile nms module
```bash
cd detector/YOLOv3/nms
sh build.sh
cd ../../..
```

## Installation using Dockerfile
Build the docker images using:
```bash
docker build -t detector . 
```

