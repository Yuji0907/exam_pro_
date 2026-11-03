from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QPainterPath, QRegion
from PyQt5.QtCore import Qt


class RoundedImage(QLabel):
    def __init__(self, image_path, radius=(20,20)):
        super().__init__()
        size = self.size()
        self.setFixedSize(size.width(), 200)

        pixmap = QPixmap(image_path)

        self.setPixmap(
            pixmap.scaled(
                size.width(),
                200,
                Qt.KeepAspectRatioByExpanding,
                   Qt.SmoothTransformation
            )
        )


        self.setStyleSheet("""
            QLabel {
                border-radius: 20px;
                background: transparent;
            }
        """)