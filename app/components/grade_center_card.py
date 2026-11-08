from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QHBoxLayout,QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path
from models.center_view_model import Center_model
# from views.center_view import Center_model
from utils.helper import clear_layout

class Grade_center_card(QWidget):

    clicked = pyqtSignal()  
    
    def __init__(self,center:Center_model,on_click=None ):
        super().__init__()

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())

        self.setObjectName("Card")
        self.setAttribute(Qt.WA_StyledBackground, True)  # lets QSS background/border apply to a plain QWidget
        self.setCursor(Qt.PointingHandCursor)

        self.on_click = on_click

        self.center:Center_model= center
        self.layout = QVBoxLayout(self)
        self.willayas_layout = QHBoxLayout(self)
        if self.center is not None:
            self.label = QLabel(self.center.center)
            self._refresh()
            self.layout.addWidget(self.label)
            
        self.layout.addLayout(self.willayas_layout)
        
    def _refresh(self):
        clear_layout(self.willayas_layout)
        for index,willaya in enumerate(self.center.willayas): 
            willaya_btn = QPushButton(willaya.willaya)
            willaya_btn.clicked.connect(lambda _,x=index:self.remove_willaya(x))
            willaya_btn.setObjectName("WillayaPill")        
            self.willayas_layout.addWidget(willaya_btn)

    def remove_willaya(self,willaya):
        print(willaya)
        self.center.willayas.pop(willaya)
        self.center.willayas=self.center.willayas
        print(self.center.willayas)
        self._refresh()

        # self.center.willayas.remove(willaya.data)
    
    
        


    def add_willaya(self,willaya):
        lable  = QLabel(willaya)
        lable.setObjectName("WillayaPill")
        self.willayas_layout.addWidget(self.label)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            if self.on_click:
                self.on_click()
        super().mousePressEvent(event)