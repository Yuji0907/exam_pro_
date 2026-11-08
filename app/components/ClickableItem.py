from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout,QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path


class ClickabelItem(QWidget):

    clicked = pyqtSignal()  
    def __init__(self, number=None, text=None, on_click=None,):
        super().__init__()

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())

        self.setObjectName("ClickableItem")
        self.setAttribute(Qt.WA_StyledBackground, True)  # lets QSS background/border apply to a plain QWidget
        self.setCursor(Qt.PointingHandCursor)
        self._on_click = on_click


        layout = QHBoxLayout(self)
        if number is not None:
            self.number = QLabel(str(number))
            layout.addWidget(self.number)

        if text is not None:
            self.label = QLabel(text)
            layout.addWidget(self.label)


        layout.addStretch()

    def set_text_style(self,style_class):
        self.label.setObjectName(style_class)

    def _clicked(self):
        self._on_click()
        
    def set_onclick(self,on_click):
        self._on_click = on_click
        self.btn.clicked.connect(self._on_click)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            if self._on_click:
                self._on_click()
        # self.label.mousePressEvent(event)
        super().mousePressEvent(event)