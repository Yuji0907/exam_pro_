from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QTableWidget, QTableWidgetItem,QHBoxLayout,QFrame
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator


from pathlib import Path

class SideBar(QFrame):
    def __init__(self, parent=None ):
        super().__init__(parent)
        style_path = Path(__file__).parent.parent  / "styles" / "components.qss"
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)
