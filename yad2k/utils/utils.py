"""Draw predicted or ground truth boxes on input image."""
import imghdr
import colorsys
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras import backend as K

from functools import reduce

def preprocess_image(img_path, model_image_size):
    image_type = imghdr.what(img_path)
    image = Image.open(img_path)
    resized_image = image.resize(tuple(reversed(model_image_size)), Image.BICUBIC)
    image_data = np.array(resized_image, dtype='float32')
    image_data /= 255.
    image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
    return image, image_data

def compose(*funcs):
    """Compose arbitrarily many functions, evaluated left to right.

    Reference: https://mathieularose.com/function-composition-in-python/
    """
    # return lambda x: reduce(lambda v, f: f(v), funcs, x)
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')

def read_classes(classes_path):
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names

def read_anchors(anchors_path):
    with open(anchors_path) as f:
        anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        anchors = np.array(anchors).reshape(-1, 2)
    return anchors

def scale_boxes(boxes, image_shape):
    """ Scales the predicted boxes in order to be drawable on the image"""
    height = float(image_shape[0])
    width = float(image_shape[1])
    image_dims = K.stack([height, width, height, width])
    image_dims = K.reshape(image_dims, [1, 4])
    boxes = boxes * image_dims

    print("Inside scale boxes")
    print(boxes)
    return boxes

def get_colors_for_classes(num_classes):
    """Return list of random colors for number of classes given."""
    # Use previously generated colors if num_classes is the same.
    if (hasattr(get_colors_for_classes, "colors") and
            len(get_colors_for_classes.colors) == num_classes):
        return get_colors_for_classes.colors

    hsv_tuples = [(x / num_classes, 1., 1.) for x in range(num_classes)]
    colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
    colors = list(
        map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
            colors))
    random.seed(10101)  # Fixed seed for consistent colors across runs.
    random.shuffle(colors)  # Shuffle colors to decorrelate adjacent classes.
    random.seed(None)  # Reset seed to default.
    get_colors_for_classes.colors = colors  # Save colors for future calls.
    return colors


# def draw_boxes(image, boxes, box_classes, class_names, scores=None):
#     """Draw bounding boxes on image.

#     Draw bounding boxes with class name and optional box score on image.

#     Args:
#         image: An `array` of shape (width, height, 3) with values in [0, 1].
#         boxes: An `array` of shape (num_boxes, 4) containing box corners as
#             (y_min, x_min, y_max, x_max).
#         box_classes: A `list` of indicies into `class_names`.
#         class_names: A `list` of `string` class names.
#         `scores`: A `list` of scores for each box.

#     Returns:
#         A copy of `image` modified with given bounding boxes.
#     """
#     #image = Image.fromarray(np.floor(image * 255 + 0.5).astype('uint8'))

#     font = ImageFont.truetype(
#         font='font/FiraMono-Medium.otf',
#         size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
#     thickness = (image.size[0] + image.size[1]) // 300

#     colors = get_colors_for_classes(len(class_names))

#     for i, c in list(enumerate(box_classes)):
#         box_class = class_names[c]
#         box = boxes[i]
        
#         if isinstance(scores.numpy(), np.ndarray):
#             score = scores.numpy()[i]
#             label = '{} {:.2f}'.format(box_class, score)
#         else:
#             label = '{}'.format(box_class)

#         draw = ImageDraw.Draw(image)
#         label_size = draw.textsize(label, font)

#         top, left, bottom, right = box
#         top = max(0, np.floor(top + 0.5).astype('int32'))
#         left = max(0, np.floor(left + 0.5).astype('int32'))
#         bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
#         right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
#         print(label, (left, top), (right, bottom))

#         if top - label_size[1] >= 0:
#             text_origin = np.array([left, top - label_size[1]])
#         else:
#             text_origin = np.array([left, top + 1])

#         # My kingdom for a good redistributable image drawing library.
#         for i in range(thickness):
#             draw.rectangle(
#                 [left + i, top + i, right - i, bottom - i], outline=colors[c])
#         draw.rectangle(
#             [tuple(text_origin), tuple(text_origin + label_size)],
#             fill=colors[c])
#         draw.text(text_origin, label, fill=(0, 0, 0), font=font)
#         del draw

#     return np.array(image)


def draw_boxes(image, boxes, box_classes, class_names, scores=None):
    """Draw bounding boxes on image.

    Draw bounding boxes with class name and optional box score on image.

    Args:
        image: An `array` of shape (width, height, 3) with values in [0, 1].
        boxes: An `array` of shape (num_boxes, 4) containing box corners as
            (y_min, x_min, y_max, x_max).
        box_classes: A `list` of indicies into `class_names`.
        class_names: A `list` of `string` class names.
        `scores`: A `list` of scores for each box.

    Returns:
        A copy of `image` modified with given bounding boxes.
    """
    #image = Image.fromarray(np.floor(image * 255 + 0.5).astype('uint8'))

    font = ImageFont.truetype(
        font='font/FiraMono-Medium.otf',
        size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
    thickness = (image.size[0] + image.size[1]) // 300

    colors = get_colors_for_classes(len(class_names))

    for i, c in list(enumerate(box_classes)):
        box_class = class_names[c]
        box = boxes[i]
        
        if isinstance(scores.numpy(), np.ndarray):
            score = scores.numpy()[i].item()
            label = f"{box_class} {score:.2f}"
        else:
            label = f"{box_class}"

        draw = ImageDraw.Draw(image)

        top, left, bottom, right = box
        top = max(0, np.floor(top + 0.5).astype('int32'))
        left = max(0, np.floor(left + 0.5).astype('int32'))
        bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
        right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
    
        coords = draw.textbbox((left + i, top + i), label, font=font)
        label_size = np.array([coords[2] - coords[0], coords[3] - coords[1]])
        if top - label_size[1] >= 0:
            text_origin = np.array([left, top - label_size[1]])
        else:
            text_origin = np.array([left, top + 1])

        for i in range(thickness):
            if left + i > right - i or top + i > bottom - i:
                continue 
            draw.rectangle(
                [(left + i, top + i), (right - i, bottom - i)], outline=colors[c])
        draw.rectangle(
            [tuple(text_origin), tuple(text_origin + label_size)],
            fill=colors[c])
        draw.text(text_origin, label, fill=(0, 0, 0), font=font)
        del draw

    return np.array(image)



# def draw_boxes(image, boxes, box_classes, class_names, scores=None):
#     """Draw bounding boxes on image.

#     Draw bounding boxes with class name and optional box score on image.

#     Args:
#         image: An `array` of shape (width, height, 3) with values in [0, 1].
#         boxes: An `array` of shape (num_boxes, 4) containing box corners as
#             (y_min, x_min, y_max, x_max).
#         box_classes: A `list` of indices into `class_names`.
#         class_names: A `list` of `string` class names.
#         `scores`: A `list` of scores for each box.

#     Returns:
#         A copy of `image` modified with given bounding boxes.
#     """
#     font = ImageFont.truetype(
#         font='font/FiraMono-Medium.otf',
#         size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
#     thickness = (image.size[0] + image.size[1]) // 300

#     colors = get_colors_for_classes(len(class_names))

#     for i, c in list(enumerate(box_classes)):
#         box_class = class_names[c]
#         box = boxes[i]
        
#         if isinstance(scores.numpy(), np.ndarray):
#             score = scores.numpy()[i]
#             label = '{} {:.2f}'.format(box_class, score)
#         else:
#             label = '{}'.format(box_class)

#         draw = ImageDraw.Draw(image)
#         label_size = draw.textbbox((0, 0), label, font=font)
        
#         # Calculate the label width and height
#         label_width = label_size[2] - label_size[0]
#         label_height = label_size[3] - label_size[1]

#         top, left, bottom, right = box
#         top = max(0, np.floor(top + 0.5).astype('int32'))
#         left = max(0, np.floor(left + 0.5).astype('int32'))
#         bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
#         right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
        
#         # Debugging Output
#         print(f"Initial Box coordinates: top={top}, left={left}, bottom={bottom}, right={right}")

#         # Ensure that y1 >= y0 and x1 >= x0
#         if top >= bottom:
#             print(f"Skipping box because top >= bottom: top={top}, bottom={bottom}")
#             continue
#         if left >= right:
#             print(f"Skipping box because left >= right: left={left}, right={right}")
#             continue

#         print(f"Adjusted Box coordinates: top={top}, left={left}, bottom={bottom}, right={right}")

#         if top - label_height >= 0:
#             text_origin = np.array([left, top - label_height])
#         else:
#             text_origin = np.array([left, top + 1])

#         # Draw the box and label
#         for i in range(thickness):
#             draw.rectangle(
#                 [left + i, top + i, right - i, bottom - i], outline=colors[c])
#         draw.rectangle(
#             [tuple(text_origin), tuple(text_origin + np.array([label_width, label_height]))],
#             fill=colors[c])
#         draw.text(text_origin, label, fill=(0, 0, 0), font=font)
#         del draw

#     return np.array(image)

