import json
import logging
import cv2
import argparse
from detector import build_detector
from utils.parser import get_config
import base64
import paho.mqtt.client as mqtt
import base64

detector = None

class Server:
    broker_address = "broker.mqtt-dashboard.com"
    #broker_address = "mqtt.eclipse.org"
    def __init__(self,args):
        print('Creating new instance')
        self.client = mqtt.Client("ObjectDetector")
        self.client.on_message = self.on_message  # attach function to callback
        self.client.connect(self.broker_address)  # connect to broker
        print("Subscribing to topic Camera")
        self.client.subscribe("fumSmartClassIot/camera")
        cfg = get_config()
        cfg.merge_from_file(args.config_detection)
        self.detector = build_detector(cfg, use_cuda=False)

    def on_message(self,client,userdata, message):
        print('getting data...')
        data = json.loads(message.payload)

        encode_image = data['encode_image']
        time_stamp = data['time_stamp']
        class_id = data['class_id']
        image = base64.b64decode(encode_image.encode('utf-8'))
        with open(f'input/{class_id}.jpg', 'wb') as f:
            f.write(image)
        ori_im = cv2.imread(f'input/{class_id}.jpg')
        im = cv2.cvtColor(ori_im, cv2.COLOR_BGR2RGB)
        # do detection
        bbox_xywh, cls_conf, cls_ids = self.detector(im)
        is_person_list = cls_ids == 0
        found_person = is_person_list.any()
        if found_person:
            print('Found')
        else:
            print('Not found')
        mask = cls_ids == 0
        bbox_xywh = bbox_xywh[mask]
        # bbox dilation just in case bbox too small, delete this line if using a better pedestrian detector
        bbox_xywh[:, 3:] *= 1.2
        for i, c in enumerate(cls_ids):
            if c == 0:

                x1, y1, w, h = bbox_xywh[i]
                x2 = int(x1 + (w / 2))
                y2 = int(y1 + (h / 2))

                x1 = int(x1 - (w / 2))
                y1 = int(y1 - (h / 2))
                cv2.rectangle(im, (x1, y1), (x2, y2), (255, 255, 255), 3)
        im = cv2.cvtColor(im,cv2.COLOR_RGB2BGR)
        cv2.imwrite(f'output/{class_id}.jpg',im)

if __name__ == '__main__':
#    logger = logging.Logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_detection", type=str, default="./configs/yolov3.yaml")
    # parser.add_argument("--ignore_display", dest="display", action="store_false", default=True)
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--frame_interval", type=int, default=1)
    parser.add_argument("--display_width", type=int, default=800)
    parser.add_argument("--display_height", type=int, default=600)
    parser.add_argument("--save_path", type=str, default="./output/")
    parser.add_argument("--cpu", dest="use_cuda", action="store_false", default=True)
    parser.add_argument("--camera", action="store", dest="cam", type=int, default="-1")
    args =  parser.parse_args()

    server = Server(args)

    rc = 0  # start the loop
    while rc == 0:
        rc = server.client.loop()
import subprocess

pid = subprocess.run('python3 camera.py')
