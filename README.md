# iDetect
### Introduction
Welcome to iDetect—a cutting-edge Python desktop application that revolutionizes object detection with state-of-the-art technology. Harnessing the power of PyQt6, TensorFlow, and OpenCV, iDetect brings the future of real-time object recognition to your fingertips.

iDetect leverages the groundbreaking You Only Look Once (YOLO) algorithm, as detailed in the acclaimed paper [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/pdf/1506.02640), to deliver unmatched accuracy and speed in detecting objects. Whether you’re processing images, videos, or capturing live footage from your camera, iDetect ensures seamless and efficient detection with its robust deep neural network.

Dive into a world where advanced object detection is both accessible and efficient—iDetect is your gateway to the next generation of computer vision.
### Project Support Features
* Handle and analyze both image and video files for precise object detection.
* Instant object detection through live camera feeds.
### Installation Guide
* Clone this repository [here](https://github.com/karti358/iDetect.git).
* The main branch is the most stable branch at any given time, ensure you're working from it.
* Ensure you create a virtual environment and activate the environment
* Open Terminal in your working directory
* ## Clone Repository and cd to it
      git clone https://github.com/karti358/iDetect.git
      cd iDetect
* ## Create Virtual Environment
      python -m venv venv
* ## Activate virtual environment
  ## Linux
      source ./venv/bin/activate
  ## Windows
      ./venv/Scripts/activate
* ## Run the following command to install all dependencies
      pip install -r requirements.txt
* Download following file [data.zip](https://www.mediafire.com/file/6xc8mhm80pungv2/data.zip/file) , unzip it, and include the model_data directory within the data directory to "iDetect" directory.
### Usage
* ## Run the following command to start the application.
      python app.py
### Usage Examples
* ## Image Processing
https://github.com/user-attachments/assets/bf32ed63-7f4f-494a-bf6e-71f64a6715ca
* ## Video Processing
https://github.com/user-attachments/assets/4000f418-c9c4-4337-8980-9f6247c7ab34
* ## Camera
https://github.com/user-attachments/assets/1ce8ee84-9f6c-4f63-8c1a-a6dbc3a1f0f3
### Technologies Used
* [PyQt6](https://doc.qt.io/qtforpython-6/index.html#)
* [Tensorflow](https://www.tensorflow.org/api_docs/python/tf)
* [Opencv](https://docs.opencv.org/4.x/index.html)
* [Matplotlib](https://matplotlib.org/)
### License
This project is available for use under the Apache 2.0 License.
