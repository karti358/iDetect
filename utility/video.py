from .utility import predict_result
from pathlib import Path
import cv2
import shutil

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

from PyQt6 import QtMultimedia
from PyQt6 import QtMultimediaWidgets

class VideoFileCard(QtWidgets.QFrame):
    def __init__(self, storage="temp_data", parent=None):
        super().__init__(parent)
        self.storage = storage
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

        self.fileUI()

    def fileUI(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.detail_label = QtWidgets.QLabel(self)
        self.detail_label.setText("Select a Video file to process.")
        self.main_layout.addWidget(self.detail_label)
        self.main_layout.setAlignment(self.detail_label, QtCore.Qt.AlignmentFlag.AlignCenter)

        # File Layout
        self.file_layout = QtWidgets.QHBoxLayout(self)

        self.file_path = QtWidgets.QLabel(self)
        self.file_path.setText("Please select a file")
        self.file_layout.addWidget(self.file_path)
        self.file_layout.setAlignment(self.file_path, QtCore.Qt.AlignmentFlag.AlignTop)
        
        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setText("Select a file.")
        self.file_button.setFixedSize(100, 30)
        self.file_button.clicked.connect(self.open_file)
        self.file_layout.addWidget(self.file_button)
        self.file_layout.setAlignment(self.file_button, QtCore.Qt.AlignmentFlag.AlignTop)

        self.main_layout.addLayout(self.file_layout)
        # end

        # Video layout
        self.video_layout = QtWidgets.QHBoxLayout(self)

        self.original_video = QtWidgets.QLabel()
        self.video_layout.addWidget(self.original_video)
        self.video_layout.setAlignment(self.original_video, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.processed_video = QtWidgets.QLabel()
        self.video_layout.addWidget(self.processed_video)
        self.video_layout.setAlignment(self.processed_video, QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.video_layout)
        # end

        # Buttons layout
        self.buttons_layout = QtWidgets.QHBoxLayout(self)

        self._processed = False
        self.process_button = QtWidgets.QPushButton(self)
        self.process_button.setText("Process")
        self.process_button.setFixedSize(100, 30)
        self.process_button.clicked.connect(self.process)
        self.buttons_layout.addWidget(self.process_button)
        self.buttons_layout.setAlignment(self.process_button, QtCore.Qt.AlignmentFlag.AlignLeft)

        self._exit = False
        self.exit_button = QtWidgets.QPushButton(self)
        self.exit_button.setText("Exit")
        self.exit_button.setFixedSize(100, 30)
        self.exit_button.clicked.connect(self.set_exit)
        self.buttons_layout.addWidget(self.exit_button)
        self.buttons_layout.setAlignment(self.exit_button, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.download_button = QtWidgets.QPushButton(self)
        self.download_button.setText("Download")
        self.download_button.setFixedSize(100, 30)
        self.download_button.clicked.connect(self.download_file)
        self.buttons_layout.addWidget(self.download_button)
        self.buttons_layout.setAlignment(self.download_button, QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.buttons_layout)
        # end

    def set_exit(self):
        self._exit = True
    
    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        file_path = Path(file_path)

        if len(file_path.as_posix()):
            self.file_path.setText(file_path.as_posix())
        else:
            self.file_path.setText("")
    
    def process(self):
        if self.file_path.text() == "Please select a file":
            QtWidgets.QMessageBox.warning(self, "Invalid", f"Select video file!")
            return
        
        filename = self.file_path.text().split("/")[-1]
        self.output_file_path = Path.cwd().joinpath(self.storage).joinpath(filename).as_posix()

        self.capture = cv2.VideoCapture(self.file_path.text())
        
        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # Specify the codec
        self.writer = cv2.VideoWriter(self.output_file_path, -1, 30.0, (608, 608))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(30)  # Adjust this interval if needed
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()  # Start the timer here

    def update_frame(self):
        if self._exit:
            self.timer.stop()
            self.capture.release()
            self.writer.release()
            return
        
        ret, frame = self.capture.read()

        if ret:
            self.process_image(frame)
        else:
            self.timer.stop()
            self.capture.release()

    def process_image(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = predict_result(image)
        image = cv2.resize(image, (608, 608), cv2.INTER_CUBIC)
        self.display_video(image, res)
        
    def display_video(self, image, result):
        self.writer.write(result)

        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(image, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        pixmap_image = QtGui.QPixmap.fromImage(q_image)
        self.original_video.setPixmap(pixmap_image)
        self.original_video.setScaledContents(True)
        self.original_video.setFixedSize(pixmap_image.size())

        height, width, channel = result.shape
        bytes_per_line = 3 * width
        q_result = QtGui.QImage(result, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        pixmap_result = QtGui.QPixmap.fromImage(q_result)
        self.processed_video.setPixmap(pixmap_result)
        self.processed_video.setScaledContents(True)
        self.processed_video.setFixedSize(pixmap_result.size())
    
    def download_file(self):
        if not self._processed:
            QtWidgets.QMessageBox.warning(self, "Invalid", f"Process video first!")
            return
        
        if not self._exit:
            QtWidgets.QMessageBox.warning(self, "Invalid", f"Exit video processing first!")
            return

        source_file = Path(self.output_file_path)
        save_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", source_file.name)

        if save_path:
            save_path = Path(save_path)
            try:
                # Copy the file to the selected location
                shutil.copy(source_file, save_path)
                QtWidgets.QMessageBox.information(self, "Success", f"File saved to {save_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
        else:
            QtWidgets.QMessageBox.warning(self, "Cancelled", "Download cancelled")