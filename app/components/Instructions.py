from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QTableWidget, QTableWidgetItem,QHBoxLayout,QFrame

from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt

from pathlib import Path

class Instructions(QFrame):
    def __init__(self, parent=None ):
        super().__init__(parent)
        style_path = Path(__file__).parent.parent  / "styles" / "Card.qss"
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)
        # self.setObjectName("Card")

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.addStretch()


        instructions = [
            (".1", "Enter the student's name"),
            (".2", "Scan the barcode"),
            (".3", "Enter the grade"),
            (".4", "Press Save"),
        ]

        for number, text in instructions:
            row = QHBoxLayout()
            row.setSpacing(10)

            number_label = QLabel(number)
            number_label.setObjectName("Instructions")

            text_label = QLabel(text)
            text_label.setObjectName("Instructions")

            number_label.setFixedWidth(30)

            row.addStretch()
            row.addWidget(text_label)
            row.addWidget(number_label)
            self.mainLayout.addLayout(row)


        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch()
        # self.mainLayout.addLayout
        