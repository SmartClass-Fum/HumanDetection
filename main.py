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
        print('getting image')
        img = base64.b64decode(message.payload)
        with open('mqtt.jpg','wb') as f:
            f.write(img)
        ori_im = cv2.imread('input/input.png')
        im = cv2.cvtColor(ori_im, cv2.COLOR_BGR2RGB)
        # do detection
        bbox_xywh, cls_conf, cls_ids = self.detector(im)
        is_person_list = cls_ids == 0
        found_person = is_person_list.any()
        if found_person:
            print('Found ')

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

    server.client.loop()  # start the loop
    while True:
        pass
