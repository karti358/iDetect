from .utility import predict_result
import cv2
import numpy as np
from pathlib import Path
import shutil

from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore

from PyQt6 import QtMultimedia
from PyQt6 import QtMultimediaWidgets

class CameraCard(QtWidgets.QFrame):
    def __init__(self, storage ="temp_data", parent=None):
        super().__init__(parent)
        self.storage=storage
        self.initUI()
    
    def initUI(self):
        self.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setStyleSheet("""
            QFrame {
                background-color: black;
                border-radius: 10px;
                padding: 15px;
            }
            
        """)

        self.launchCamera()

    def launchCamera(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.image_label = QtWidgets.QLabel()
        self.main_layout.addWidget(self.image_label)
        self.main_layout.setAlignment(self.image_label, QtCore.Qt.AlignmentFlag.AlignCenter)

        # button layout
        self.button_layout = QtWidgets.QHBoxLayout(self)

        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.clicked.connect(self.set_exit)
        self.exit_button.setFixedSize(100, 30)
        self.button_layout.addWidget(self.exit_button)
        self.button_layout.setAlignment(self.exit_button, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)

        self.capture_button = QtWidgets.QPushButton(self)
        self.capture_button.setText("Capture")
        self.capture_button.clicked.connect(self.capture)
        self.capture_button.setFixedSize(100, 30)
        self.button_layout.addWidget(self.capture_button)
        self.button_layout.setAlignment(self.capture_button, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.setAlignment(self.button_layout, QtCore.Qt.AlignmentFlag.AlignBottom)
        # end

        self.camera = cv2.VideoCapture(0)
        self._exit = False

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.image_capture)
        self.timer.start(100)
    
    def image_capture(self,):
        if not self._exit:
            ret, frame = self.camera.read()
            self.process_image(frame)
        else:
            self.camera.release()

    def set_exit(self):
        self._exit = True

    def process_image(self, frame):
        # if not self.camera.isOpened():
        #     self.capture()
        #     return

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = predict_result(image)
        self.display_image(self.result)
    
    def capture(self):
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "image.jpg")

        if save_path:
            save_path = Path(save_path)
            try:
                cv2.imwrite(save_path.as_posix(), self.result)
                QtWidgets.QMessageBox.information(self, "Success", f"File saved to {save_path.as_posix()}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Cancelled", "Download cancelled")

    def display_image(self, image):
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(image, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(pixmap.size())
