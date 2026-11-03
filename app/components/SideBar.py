from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QTableWidget, QTableWidgetItem,QHBoxLayout,QFrame
from PyQt5.QtCore import QThread, pyqtSignal
from db.database import Database
from db.schemas import (CANDIDATES,EVAL)
from PyQt5.QtGui import QPixmap
from gui.components.CheckRow import CheckRow
from gui.components.RoundedImage import RoundedImage
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from codeBar.CameraScanner import scanLoop
from PyQt5.QtGui import QIntValidator
from controller.candidates import CandidatesController
from controller.batchs import BatchsController
db = Database()

from pathlib import Path
class Worker(QThread):
    finished = pyqtSignal()
    code_detected = pyqtSignal(str)

    def run(self):
        scanLoop(self.code_detected)
        self.finished.emit()
class SideBar(QFrame):

    def __init__(self, parent=None ):
        super().__init__(parent)
        style_path = Path(__file__).parent.parent  / "styles" / "components.qss"
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)
        self.setObjectName("Card")
        self.candidates_con = CandidatesController()
        self.batchsController = BatchsController()
        worker = Worker()
        worker.code_detected.connect(lambda res:self.Scaned(res))
        worker.start()

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)

        image = RoundedImage(
            "scanBackground.png",
            radius=(0,25)
        )

        self.mainLayout.addWidget(image)


        # ==========================================
        # title
        # ==========================================

        self.title = QLabel("تسجيل النقاط")
        self.title.setObjectName("SideBarTitle")
        title_row = QHBoxLayout()
        # title_row.addStretch()
        title_row.addStretch()
        title_row.addWidget(self.title)
        title_row.addStretch()
        self.mainLayout.addLayout(title_row)

        # self.mainLayout.addStretch()    


        # ==========================================
        # checks
        # ==========================================
        self.check1 = CheckRow("Scanner connected")
        self.check1.check()
        self.check2 = CheckRow("Candidate identified")
        self.check3 = CheckRow("Evaluation completed")
        self.check4 = CheckRow("Data saved")
        self.packet_number = CheckRow("packet number")

        self.mainLayout.addWidget(self.check1)
        self.mainLayout.addWidget(self.check2)
        self.mainLayout.addWidget(self.check3)
        self.mainLayout.addWidget(self.check4)
        self.mainLayout.addWidget(self.packet_number)

        self.message = QLabel("Student found successfully.")
        self.message.setWordWrap(True)


        self.mainLayout.addStretch()    





        # ==========================================
        # input text 
        # =========================================
        self.input_default_stylSheet = """
                QLineEdit {
                    border-radius:10px;
                    padding:10px;
                    border:1px solid gray;
                }
            """

        self.input_field = QLineEdit()
        self.input_field.setStyleSheet(self.input_default_stylSheet)
        self.input_field.setFixedSize(round(self.width()*.7), 51)
        self.input_field.setDisabled(True)
        self.input_field.setPlaceholderText("enter grade between 0 and 20")
        self.input_field.textChanged.connect(self.Grade_validator)

        input_row = QHBoxLayout()        
        input_row.addStretch()
        input_row.addWidget(self.input_field)
        input_row.addStretch()

        self.mainLayout.addLayout(input_row)


        # ==========================================
        # Done button
        # =========================================

        self.button = QPushButton("Done")
        self.button.setObjectName("Button")
        self.button.setFixedWidth(200)
        self.button.setDisabled(True)
        button_row = QHBoxLayout()        
        button_row.addStretch()
        button_row.addWidget(self.button)
        button_row.addStretch()
        



        self.mainLayout.addLayout(button_row,)
        self.button.clicked.connect(self.evaluate)

        self.setLayout(self.mainLayout)
        self.mainLayout.addStretch()    
        self.mainLayout.addStretch()

        # self.mainLayout.addLayout
    def Grade_validator(self,text):
        if not text:
            return
        try:
            value = float(text)
        except ValueError:
            self.input_field.clear()
            return
        if value > 20 or value <0  :
            self.input_field.backspace()
            self.input_field.setStyleSheet("""
                QLineEdit {
                    border:1px solid red;
                    border-radius:10px;
                    padding:10px;
                }
            """)
        else:
                    self.input_field.setStyleSheet("""
                QLineEdit {
                    border:1px solid green;
                    border-radius:10px;
                    padding:10px;
                }
            """)
    def Scaned(self,res):
        self.check3.checkOut()
        self.check4.checkOut()
        self.packet_number.checkOut()

        # self.hash_id.setText(res )
        self.button.setDisabled(False)
        self.input_field.setDisabled(False)
        self.input_field.setText("")
        self.candidate=res
        self.check2.check(res)

    # def get_Packect_number(self):
    
    def evaluate(self):
        self.check2.checkOut()
        self.check3.check(self.input_field.text())
        grade =float(self.input_field.text())
        self.candidates_con.evaluate_candidate(hash_id=self.candidate,grade=grade)
        backet_number = self.batchsController.get_batch_name(hash_id=self.candidate)
        self.check4.check(self.input_field.text())
        self.packet_number.check(backet_number[0])
        self.input_field.setDisabled(True)
        self.button.setDisabled(True)
        self.input_field.setStyleSheet(self.input_default_stylSheet)
