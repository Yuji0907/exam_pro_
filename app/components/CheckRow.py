from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from pathlib import Path

class CheckRow(QWidget):
    def __init__(self, text,
                  check_icon="assets/icons/check.png",
                  check_icon_error="assets/icons/check_with_error.png" ):
        super().__init__()
        style_path = Path(__file__).parent.parent  / "styles" / "components.qss"
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)
        self.scan_res_stylSheet = """
                QLabel {
                    color:green;
                    font-size : 18px;
                    background-color: white;    
                }
            """
        self.scan_error_stylSheet = """
                QLabel {
                    color:red;
                    font-size : 18px;
                    background-color: white;    
                }
            """
        self.scan_res_disabled_stylSheet = """
                QLabel {
                color:gray;
                font-size : 18px;
                background-color: white;
                }
            """
        self.icon = QLabel()
        self.icon.setObjectName("Checks")
        
        self.label = QLabel(text)
        self.label.setObjectName("Checks")

        self.message = QLabel("")
        self.message.setObjectName("ChekMessage")

        # Load pixmap
        self.checkIconError = QPixmap(check_icon_error)
        self.checkIcon = QPixmap(check_icon)
        self.message.setStyleSheet(self.scan_res_disabled_stylSheet)
        # Icon size
        self.icon.setFixedSize(30, 30)

        # Scale image
        self.checkIcon = self.checkIcon.scaled(
            30,
            30,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.checkIconError = self.checkIconError.scaled(
            20,
            20,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.icon.setPixmap(self.checkIcon)
        self.icon.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(50,0,0,0)
        layout.addWidget(self.icon)
        layout.addWidget(self.label)
        layout.addWidget(self.message)
        layout.addStretch()

        # Disabled by default
        self.setEnabled(False)

    def check(self,message=""):
        self.message.setEnabled(True)
        self.message.setText(str(message))
        # self.icon.setPixmap(self.checkIconError)
        self.setEnabled(True)
        self.message.setStyleSheet(self.scan_res_stylSheet)

    def error(self,message=""):
        self.message.setEnabled(True)
        self.message.setText(str(message))
        self.icon.setPixmap(self.checkIconError)
        self.setEnabled(True)
        self.message.setStyleSheet(self.scan_error_stylSheet)

    def checkOut(self,message=""):
        self.message.setStyleSheet(self.scan_res_disabled_stylSheet)
        # self.message.setText(message)
        self.setEnabled(False)
        self.message.setEnabled(False)