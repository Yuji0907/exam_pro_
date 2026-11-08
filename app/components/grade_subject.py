from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt, pyqtSignal
from pathlib import Path
from models.subject_grade_model import Subject_grade
from models.subject_model import SubjectModel

class Grade_subject_card(QWidget):

    clicked = pyqtSignal()  
    
    def __init__(self,subject_grade:Subject_grade,on_click=None ):
        super().__init__()

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())

        self.setObjectName("SubjectGradeCard")
        self.setAttribute(Qt.WA_StyledBackground, True)  # lets QSS background/border apply to a plain QWidget
        self.setCursor(Qt.PointingHandCursor)

        self.on_click = on_click

        self.subject_grade= subject_grade
        self.layout = QVBoxLayout(self)
        

        if self.subject_grade is not None:
            self.label = QLabel(self.subject_grade.grade.name)
            self.layout.addWidget(self.label)
            
            for subject in subject_grade.subjects:
                self.subject_lable = QLabel(subject.subject)
                
                # coeff ------
                subject_coeff = QLineEdit()
                subject_coeff.setPlaceholderText("1..4")
                print(subject.coeff)
                if not(subject.coeff == 0):
                    subject_coeff.setText(str(subject.coeff))
                subject_coeff.setValidator(QIntValidator(0, 4, self))
                subject_coeff.textChanged.connect(
                    lambda value, current_subject=subject: self._update_subject_coeff(current_subject, value)
                )

                #------layout-----------
                subjects_column = QWidget()
                subjects_layout = QVBoxLayout()
                subjects_column.setLayout(subjects_layout)
                subjects_layout.addWidget(self.subject_lable)
                subjects_layout.addWidget(subject_coeff)

                self.layout.addWidget(subjects_column)
            
    @staticmethod
    def _update_subject_coeff(subject: SubjectModel, value: str) -> None:
        subject.coeff = int(value) if value else 0


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
            if self.on_click:
                self.on_click()
        super().mousePressEvent(event)