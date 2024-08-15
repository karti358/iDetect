import sys
import os
import shutil
from functools import partial

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6 import QtGui

from utility.image import ImageFileCard
from utility.video import VideoFileCard
from utility.camera import CameraCard

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, storage="temp_data"):
        super().__init__()
        self.storage=storage
        self.initUI()
        
    def initUI(self):
        self.setGeometry(400, 200, 800, 500)
        self.set_style()

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.add_buttons()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.clear_storage)
        self.timer.start(900000) # Every 15 minutes.

    def set_style(self):
        self.setStyleSheet(
            """
            QMainWindow{
                background-color: #3C4043 ;
            }

            QPushButton {
                background-color: #808b96;

            }
            """
        )
    
    def add_buttons(self):
        self.button_layout = QtWidgets.QHBoxLayout()

        self.refresh = QtWidgets.QPushButton("Refresh", self)
        self.refresh.setFixedSize(100, 30)
        self.refresh.clicked.connect(self.refresh_layout)
        self.button_layout.addWidget(self.refresh)

        self.image_button = QtWidgets.QPushButton("Image", self)
        self.image_button.setFixedSize(100, 30)
        self.image_button.clicked.connect(partial(self.add_widget, "image"))
        self.button_layout.addWidget(self.image_button)

        self.video_button = QtWidgets.QPushButton("Video", self)
        self.video_button.setFixedSize(100, 30)
        self.video_button.clicked.connect(partial(self.add_widget, "video"))
        self.button_layout.addWidget(self.video_button)

        self.camera_button = QtWidgets.QPushButton("Camera", self)
        self.camera_button.setFixedSize(100, 30)
        self.camera_button.clicked.connect(partial(self.add_widget, "camera"))
        self.button_layout.addWidget(self.camera_button)

        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_layout.setSpacing(0)

        self.main_layout.addLayout(self.button_layout)
        self.main_layout.setAlignment(self.button_layout, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
    
    def add_widget(self, option):
        if option == "image":
            card = ImageFileCard()
        elif option == "video":
            card = VideoFileCard()
        elif option == "camera":
            card = CameraCard()

        self.refresh_layout()
        self.main_layout.addWidget(card)
    
    def clear_storage(self):
        for item in os.listdir(self.storage):
            if item == ".gitkeep":
                continue
            item_path = f"{self.storage}/{item}"
            if os.path.isfile(item_path):
                os.remove(item_path)
            else:
                shutil.rmtree(item_path)

    def refresh_layout(self):
        self.clear_storage()
        for i in reversed(range(self.main_layout.count())): 
            widget = self.main_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()  # Remove and delete the widget

        # Re-add the button layout
        self.main_layout.addLayout(self.button_layout)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("iDetect")
window.setWindowIcon(QtGui.QIcon("app_data/app_logo.png"))
window.show()

sys.exit(app.exec())
