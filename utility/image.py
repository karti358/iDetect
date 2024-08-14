from .utility import process
from pathlib import Path
import cv2
import shutil

from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore

class ImageFileCard(QtWidgets.QFrame):
    def __init__(self, storage="temp_data", parent=None):
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
            
            QLabel {
                padding: 0px 0px;
            }
        """)

        self.fileUI()

    def fileUI(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.detail_label = QtWidgets.QLabel(self)
        self.detail_label.setText("Select an Image file to process.")
        self.main_layout.addWidget(self.detail_label)
        self.main_layout.setAlignment(self.detail_label, QtCore.Qt.AlignmentFlag.AlignCenter)

        # File Layout
        self.file_layout = QtWidgets.QHBoxLayout(self)

        self.file_path = QtWidgets.QLabel(self)
        self.file_path.setText("Please select a file")
        self.file_layout.addWidget(self.file_path)
        self.file_layout.setAlignment(self.file_path, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        
        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setText("Select a file.")
        self.file_button.setFixedSize(100, 30)
        self.file_button.clicked.connect(self.open_file)
        self.file_layout.addWidget(self.file_button)
        self.file_layout.setAlignment(self.file_button, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.file_layout)
        # end

        # Image Layout
        self.image_label = QtWidgets.QLabel(self)
        self.main_layout.addWidget(self.image_label)
        self.main_layout.setAlignment(self.image_label, QtCore.Qt.AlignmentFlag.AlignCenter)
        #end

        # buttons layout
        self.button_layout = QtWidgets.QHBoxLayout(self)

        self._processed = False
        self.process_button = QtWidgets.QPushButton(self)
        self.process_button.setText("Process")
        self.process_button.setFixedSize(100, 30)
        self.process_button.clicked.connect(self.process)
        self.button_layout.addWidget(self.process_button)
        self.button_layout.setAlignment(self.process_button, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.download_button = QtWidgets.QPushButton(self)
        self.download_button.setText("Download")
        self.download_button.setFixedSize(100, 30)
        self.download_button.clicked.connect(self.download_file)
        self.button_layout.addWidget(self.download_button)
        self.button_layout.setAlignment(self.download_button, QtCore.Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.button_layout)
        # end
    
    def open_file(self,):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
        file_path = Path(file_path)

        if len(file_path.as_posix()):
            self.file_path.setText(file_path.as_posix())
        else:
            self.file_path.setText("")
    
    def process(self,):
        if self.file_path.text() == "Please select a file":
            QtWidgets.QMessageBox.warning(self, "Invalid", f"Select image file!")
            return
        
        filename = self.file_path.text().split("/")[-1]
        self.output_file_path = Path.cwd().joinpath(self.storage).joinpath(filename).as_posix()

        if process("image", self.file_path.text(), self.output_file_path):
            self.display_image()
        
    def display_image(self,):
        image = cv2.imread(self.output_file_path, cv2.IMREAD_COLOR)

        if image is None:
            print("Error: Image not found.")
            return
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(pixmap.size())

        self._processed = True
    
    def download_file(self):
        if not self._processed:
            QtWidgets.QMessageBox.warning(self, "Invalid", f"Process image first!")
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