from PIL import Image
import numpy as np

from yad2k.models.keras_yolo import yolo_head, yolo_eval
from yad2k.utils.utils import draw_boxes

def predict(image, anchors, class_names, yolo_model):
    yolo_model_outputs = yolo_model(image)["conv2d_22"]
    yolo_outputs = yolo_head(yolo_model_outputs, anchors, len(class_names))
    
    yolo_outputs = yolo_outputs[:-1]

    out_boxes, out_scores, out_classes = yolo_eval(yolo_outputs, np.array(image.shape[1:3], dtype=np.float32), 10, 0.3, 0.5)

    return draw_boxes(Image.fromarray(np.array(image[0, ...] * 255.0, dtype=np.uint8)), out_boxes, out_classes, class_names, out_scores)