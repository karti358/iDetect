import cv2
import numpy as np
from pathlib import Path

from yad2k.utils.utils import read_anchors
from yad2k.utils.utils import read_classes

import tensorflow as tf
from .process_image import predict

anchors = read_anchors(Path.cwd().joinpath("model_data/yolo_anchors.txt"))
classes = read_classes(Path.cwd().joinpath("model_data/coco_classes.txt"))
MODEL_PATH=Path.cwd().joinpath("model_data/yolo.keras")
yolo_model = tf.keras.models.load_model(MODEL_PATH)

def process_image(image): 
    image = cv2.resize(image, (608, 608), interpolation=cv2.INTER_CUBIC)
    image = np.array(image, dtype=np.float32) / 255.0
    image = image[np.newaxis, ...]
    return image

def process(filetype, input_file_path, output_file_path):
    global anchors, classes, yolo_model
    if filetype == "image":
        image = cv2.imread(input_file_path, cv2.IMREAD_COLOR)
        image = process_image(image)
        res = predict(image, anchors, classes, yolo_model)

        if not cv2.imwrite(output_file_path, res):
            print("Could not process file.")
            return False
        
        print("Processed file successfully.")
        return True
     
    elif filetype == "video":
        cap = cv2.VideoCapture(input_file_path)

        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        writer = cv2.VideoWriter(output_file_path, fourcc, 30.0, (608,  608))
        
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                print("Could not read video file.")
                return False
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = process_image(image)
            res = predict(image, anchors, classes, yolo_model)

            writer.write(res)
            cv2.imshow("Frame", res)

            if cv2.waitKey(1) == ord("x"):
                break
        
        cap.release()
        writer.release()

        cv2.destroyAllWindows()

        print("File processed successfully.")
        return True
    
def predict_result(image):
    global anchors, classes, yolo_model

    image = process_image(image)
    return predict(image, anchors, classes, yolo_model)