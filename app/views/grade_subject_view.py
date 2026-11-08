from pathlib import Path

from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFrame,
    QSplitter,
    QScrollArea,
    QComboBox
)
from PyQt5.QtCore import Qt
from sqlalchemy.orm import Session
from components.Item import Item
from components.ClickableItem import ClickabelItem
from components.grade_center_card import Grade_center_card
from components.grade_subject import Grade_subject_card
from controllers.subject_controller import SubjectController
from controllers.willaya_controller import WillayaController
from controllers.grade_controller import GradeController
from models.center_model import CenterModel
from models.willaya_model import WillayaModel
from models.grade_model import GradeModel
from dataclasses import dataclass
from models.subject_model import SubjectModel 
from models.willaya_model import WillayaModel
from models.subject_grade_model import Subject_grade  as Subject_grade_model

from utils.helper import clear_layout

# @dataclass
# class Center_model:
#     center_id:int
#     center:str
#     willayas:list[Willaya_model]

# @dataclass
# class Center_assingment_model:
#     id:int
#     grade:str
#     centers:list[Center_model]
#     current_center:int=None

    



class GradeSubjectView(QSplitter):
    def __init__(self, session: Session):
        super().__init__(Qt.Horizontal)
        self.setWindowTitle("subjects grades")
        self.setMinimumSize(640, 480)
        self._current_subject_grade = None
        self.subject_controller = SubjectController(view=self, session=session)
        self.grade_controller = GradeController(view=self, session=session)
        self._subjects_grades:list[Subject_grade_model]=self.subject_controller.load_grades_subjects()
        print(self._subjects_grades)
        self._current_subject_grade = 0


        SEPARATOR = "#e2e2e2"


        self.setStyleSheet(f"""
            QSplitter::handle:horizontal {{
                background-color: {SEPARATOR};
                margin: 0 1px; 
                width: 9px;
            }}
        """)



        self.resize(900, 500)




        
        grades_view = self._build_grades_view()
        subjects_view = self._build_subjects_view()
        grade_subject_view = self._build_grade_subject_view()

        # self.willaya_controller.load_willayas()

        
        self.addWidget(grades_view)  
        self.addWidget(grade_subject_view)  
        self.addWidget(subjects_view)  

        w = self.width()
        self.setSizes([w // 3, w // 3, w // 3])
        



    # -----------------------------------------------
    # grades view create and handel
    # ------------------------------------------------
    def _build_grades_view(self) -> QWidget:
        grades_view = QFrame()

        grades_mainLayout = QVBoxLayout(grades_view)
        grades_mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        grade_container = QWidget()
        self.grades_layout = QVBoxLayout(grade_container)
        self.grades_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # scroll area wrapping the container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # container resizes with the viewport
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(grade_container)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search..")
        grades_mainLayout.addWidget(search_input)
        grades_mainLayout.addWidget(scroll_area, 1)  # stretch factor 1: takes the free space
        self.grade_controller.load_grades()

        # grade name input
        self.grade_name = QLineEdit()
        self.grade_name.setPlaceholderText("name..")
        grades_mainLayout.addWidget(self.grade_name)

        add_button = QPushButton("add")
        add_button.setObjectName("CustomButton")
        add_button.clicked.connect(self._add_new_grade)
        grades_mainLayout.addWidget(add_button)

        return grades_view
    def _add_new_grade(self):
        print(self.grade_name.text())
        if self.grade_name.text() == "":
            QMessageBox.warning(
                self,
                "the grade number is missing",
                "the grade number is missing"

                )
            return 
        self.grade_controller.create_grade(self.grade_name.text())
        self.grade_controller.load_grades()

    def load_grades(self, grades: list[GradeModel]) -> None:
        clear_layout(self.grades_layout)
        print("==================")
        print(grades)
        if len(grades) == 0 :
            return
        self._gardes = {grade.id: grade for grade in grades}
        for index, grade in enumerate(grades):
            item = ClickabelItem(text =grade.name,
                          on_click=lambda x= grade :self._add_subject_grade(x))
            self.grades_layout.addWidget(item)

    def _get_current_subject_grade(self):
        if len(self._subjects_grades) == 0:
            return None
        return self._subjects_grades[self._current_subject_grade]

    def _load_subjects_grade(self):
        subjects_grade:Subject_grade_model =self._get_current_subject_grade()
        self.g_subject_layout.addWidget(Grade_subject_card(subject_grade=subjects_grade))

            # center_card = Grade_center_card(center=center,on_click=lambda :print("hello"))
            # center_card.clicked.connect(lambda x=index,y=centers_grade:self._on_center_clicked(x,y))
            # self.centers_grade_layout.addWidget(center_card)
            
    def _add_subject_grade(self,grade:GradeModel):
        clear_layout(self.g_subject_layout)
        # subjects_grades:Subject_grade_model =self._get_current_subject_grade()
        print(grade.name)
        print(grade.id)
        for indx,a in enumerate(self._subjects_grades):
            if a.id==grade.id:
                self._current_subject_grade = indx
                self._load_subjects_grade()
                return
            
        new_Subject_grade = Subject_grade_model(
            grade=grade,
            subjects=[],
            id=grade.id,
            current_subject=0,
            )
        
        self._subjects_grades.append(new_Subject_grade)
        self._current_subject_grade = len(self._subjects_grades)-1
        self._load_subjects_grade()



        #create and add new center
            

        
        

 

    # -----------------------------------------------
    # subjects  view create and handel
    # ------------------------------------------------

    def _build_subjects_view(self) -> QWidget:
        subjects_view = QFrame()

        subjects_mainLayout = QVBoxLayout(subjects_view)
        subjects_mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        subject_container = QWidget()
        self.subject_layout = QVBoxLayout(subject_container)
        self.subject_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # scroll area wrapping the container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(subject_container)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search..")
        subjects_mainLayout.addWidget(search_input)
        subjects_mainLayout.addWidget(scroll_area, 1)
        self.subject_controller.load_subjects()

        # subject name input
        self.subject_name = QLineEdit()
        self.subject_name.setPlaceholderText("name..")
        subjects_mainLayout.addWidget(self.subject_name)

        add_button = QPushButton("add")
        add_button.setObjectName("CustomButton")
        add_button.clicked.connect(self._create_new_subject)
        subjects_mainLayout.addWidget(add_button)

        return subjects_view


    def load_subjects(self, subjects: list[SubjectModel]) -> None:
        clear_layout(self.subject_layout)
        self._subjects = {subject.id: subject for subject in subjects}
        for index, subject in enumerate(subjects):
            item = QPushButton(subject.subject)
            item.data = subject
            item.clicked.connect(self.add_subject)
            self.subject_layout.addWidget(item)

    def add_subject(self):
        print("clicked")
        subjects_grade:Subject_grade_model =self._get_current_subject_grade()
        subject_data= self.sender().data
        if subject_data in  subjects_grade.subjects:
            return
        subjects_grade.subjects.append(subject_data)
        clear_layout(self.g_subject_layout)
        self._load_subjects_grade()

    def _create_new_subject(self):
        print(self.subject_name.text())
        if self.subject_name.text() == "":
            QMessageBox.warning(
                self,
                "the subject name is missing",
                "the subject name is missing"

                )
            return 
        self.subject_controller.create_subject(subject=self.subject_name.text())



    
    # -----------------------------------------------
    # subject for the garde view 
    # ------------------------------------------------
    
    def _save_subjects_grade(self):
        subjects_grade:Subject_grade_model =self._get_current_subject_grade()
        missing = [
        str(s.subject)
        for s in subjects_grade.subjects
        if (s.coeff == 0 )or str(s.coeff).strip() == ""
        ]
        if missing:
            QMessageBox.warning(
                self,
                "Missing coefficient",
                "Please enter a coefficient for:\n- " + "\n- ".join(missing),
                )
            return 
        self.subject_controller._assign_subjects_to_grade(subject_grade=subjects_grade)

    def show_error(self,e):
        QMessageBox.warning(self,"error",e)

    # def _load_subjects_grades(self) ->list[Subject_grade_model]:
            
    def _build_grade_subject_view(self) -> QWidget:
        grade_subject_view = QFrame()
        outer_layout = QVBoxLayout(grade_subject_view)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # inner widget resizes with the scroll area
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Inner container that actually holds the items
        container = QWidget()
        self.g_subject_layout = QVBoxLayout(container)
        self.g_subject_layout.setAlignment(Qt.AlignTop)  
        self._load_subjects_grade()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        save_button = QPushButton("save")
        save_button.setObjectName("CustomButton")
        save_button.clicked.connect(self._save_subjects_grade)
        outer_layout.addWidget(save_button)
        return grade_subject_view

    





