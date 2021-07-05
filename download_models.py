import os
import logging
import traceback
import gdown
import zipfile


links = {
    # YOLO3
    "https://drive.google.com/u/0/uc?id=1Vw2QljpCrqkub7unkgI-9n2I46ReEHdv&export=download": "./detector/YOLOv3/weight/yolov3.weights",
    "https://drive.google.com/u/0/uc?id=1_v_xW1V52gZCZnXgh1Ap_gwA9YVIzUnS&export=download": "./detector/YOLOv3/weight/yolov3-tiny.weights"
}

if __name__ == "__main__":
    os.makedirs('./detector/YOLOv3/weight', exist_ok=True)

    # download
    for i, (link, filename) in enumerate(links.items()):
        try:
            url = link
            output = filename
            gdown.download(url, output, quiet=False)
        except Exception as e:
            logging.error(traceback.format_exc())
