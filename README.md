# iDetect
### Introduction
iDetect is a Python based desktop application using PyQT6, Tensorflow, OpenCv-Python etc.
iDetect is a implementation of Object Detection using Deep Neural Network.
Refer the Paper - [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/pdf/1506.02640)
### Project Support Features
* Support image/video file procesing and detect objects in them.
* Camera support with real time object detection.
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
* Download following file [model_data.zip](https://www.mediafire.com/file/6xc8mhm80pungv2/model_data.zip/file) , unzip it, and include the model_data directory in root of "iDetect" directory.
### Usage
* ## Run the following command to start the application.
      python app.py
### Usage Examples
* ## Image Processing
https://github.com/user-attachments/assets/bf32ed63-7f4f-494a-bf6e-71f64a6715ca
* ## Video Processing

* ## Camera
### Technologies Used
* [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
### License
This project is available for use under the Apache 2.0 License.
