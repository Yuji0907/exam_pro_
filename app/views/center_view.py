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
from components.grade_center_card import Grade_center_card
from controllers.center_controller import CenterController
from controllers.willaya_controller import WillayaController
from controllers.grade_controller import GradeController
from models.center_model import CenterModel
from models.willaya_model import WillayaModel
from models.grade_model import GradeModel
from dataclasses import dataclass
from models.center_view_model import Center_model

@dataclass
class Willaya_model:
    id:int
    willaya:str


# @dataclass
# class Center_model:
#     center_id:int
#     center:str
#     willayas:list[Willaya_model]

@dataclass
class Center_assingment_model:
    id:int
    grade:str
    centers:list[Center_model]
    current_center:int=None

    



class CenterView(QSplitter):
    def __init__(self, session: Session):
        super().__init__(Qt.Horizontal)
        self.setWindowTitle("Centers")
        self.setMinimumSize(640, 480)
        self._current_center_assingment = None
        self._center_assignments:list[Center_assingment_model]=[]




        style_path = Path(__file__).parent.parent / "styles" / "style.qss"
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self.resize(900, 500)



        self._centers: dict[int, CenterModel] = {}
        self._editing_center_id: int | None = None
        self.controller = CenterController(view=self, session=session)
        self.willaya_controller = WillayaController(view=self, session=session)
        self.grade_controller = GradeController(view=self, session=session)
        
        centers_view = self._build_centers_view()
        center_view = self._build_center_grade_view()
        willaya_view = self._build_willaya_view()

        self.willaya_controller.load_willayas()

        
        self.addWidget(centers_view)  
        self.addWidget(center_view)  
        self.addWidget(willaya_view)  

        w = self.width()
        self.setSizes([w // 3, w // 3, w // 3])
        



    # -----------------------------------------------
    # centers   view
    # ------------------------------------------------

    def _build_centers_view(self) -> QWidget:
        SEPARATOR = "#e2e2e2"
        center_view = QFrame()

        # centers layouts 
        self.centers_layout = QVBoxLayout(center_view)
        self.centers_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setStyleSheet(f"""
            QSplitter::handle:horizontal {{
                background-color: {SEPARATOR};
                margin: 0 1px; 
                width: 9px;
            }}
        """)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search..")        
        self.centers_layout.addWidget(search_input)
        self.controller.load_centers()
        self.centers_layout.addStretch()

        # center name input 
        center_name = QLineEdit()
        # center_name.setObjectName("CustomInput")
        center_name.setPlaceholderText("name..")        
        self.centers_layout.addWidget(center_name)

        add_button = QPushButton("add")
        add_button.setObjectName("CustomButton")
        self.centers_layout.addWidget(add_button)
        return center_view


    def display_centers(self, centers: list[CenterModel]) -> None:
        self._centers = {center.id: center for center in centers}
        for index, center in enumerate(centers):
            item = Item(text =center.name,button = "add",
                        on_click=lambda x= center :self._add_center_grade(x))
            self.centers_layout.addWidget(item)



            print(center.id)
            print(center.name)



        

 

    # -----------------------------------------------
    # center grade view
    # ------------------------------------------------
    def _build_center_grade_view(self) -> QWidget:
        center_view = QFrame()
        main_layout = QVBoxLayout(center_view)
        self.centers_grade_layout = QVBoxLayout()

        # grades combo ================
        self.grade_combo = QComboBox()
        self.grade_combo.currentIndexChanged.connect(self.handle_grade_changed)
        self.grade_controller.load_grades()

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(self.grade_combo)
        main_layout.addLayout(self.centers_grade_layout)

        return center_view
    def _get_current_center_assingment(self):
        return self._center_assignments[self._current_center_assingment]

    
    def _load_centers_grade(self):
        centers_grade:Center_assingment_model =self._get_current_center_assingment()
        for index,center in enumerate(centers_grade.centers):
            center_card = Grade_center_card(center=center,on_click=lambda :print("hello"))
            center_card.clicked.connect(lambda x=index,y=centers_grade:self._on_center_clicked(x,y))
            self.centers_grade_layout.addWidget(center_card)

    def _on_center_clicked(self,index,centers_grade):
        print("clicked")
        print(index)
        centers_grade.current_center = index


    def clear_layout(self,layout):
        if layout is not None:
            while layout.count():
                item= layout.takeAt(0)
                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self.clear_layout(item.layout())


    def handle_grade_changed(self,index):
        self.clear_layout(self.centers_grade_layout)
        grade_id = int(self.grade_combo.itemData(index))
        grade = self.grade_combo.itemText(index)

        for indx,a in enumerate(self._center_assignments):
            if a.id==grade_id:
                self._current_center_assingment = indx
                self._load_centers_grade()
                return

        new_assingment = Center_assingment_model(
            id=grade_id,
            grade=grade,
            centers=[],
            current_center=0

        )
        self._center_assignments.append(new_assingment)
        self._current_center_assingment = len(self._center_assignments)-1
        self._load_centers_grade()



    def _add_center_grade(self,center):
        print(center)
        centers_grade:Center_assingment_model =self._get_current_center_assingment()

        new_center = Center_model(
            center_id=center.id,
            center=center.name,
            willayas=[]
            )
        if new_center in centers_grade.centers:
            return
        centers_grade.centers.append(new_center)

        #create and add new center
        center_card = Grade_center_card(center=new_center)
        center_card.clicked.connect(lambda x=len(centers_grade.centers)-1,y=centers_grade:self._on_center_clicked(x,y))
        self.centers_grade_layout.addWidget(center_card)
        # print(item.number.text())
    
    def load_grades(self,grades:list[GradeModel]):
        for grade in grades:
            self.grade_combo.addItem(grade.name,grade.id)
        self.grade_data= self.grade_combo.itemData(0)
    
    # -----------------------------------------------
    # willaya view
    # ------------------------------------------------
    
    def _build_willaya_view(self) -> QWidget:
        willaya_view = QFrame()
        outer_layout = QVBoxLayout(willaya_view)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # inner widget resizes with the scroll area
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Inner container that actually holds the items
        container = QWidget()
        self.willaya_layout = QVBoxLayout(container)
        self.willaya_layout.setAlignment(Qt.AlignTop)  

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        return willaya_view

    
    def load_willayas(self,willayas):
        for willaya in willayas:
            item = QPushButton(willaya.willaya) 
            item.willayaData={"id":willaya.id,"willaya":willaya.willaya}
            item.clicked.connect(self._add_willaya_to_current_center)
            self.willaya_layout.addWidget(item)

    def _add_willaya_to_current_center(self):
        centers_grade:Center_assingment_model =self._get_current_center_assingment()
        
        willaya_data= self.sender().willayaData
        current_center = centers_grade.centers[centers_grade.current_center]
        new_willaya = Willaya_model(
            id=willaya_data["id"],
            willaya=willaya_data["willaya"]
            )
        if new_willaya in current_center.willayas:
            return
        current_center.willayas.append(new_willaya)
        self.clear_layout(self.centers_grade_layout)
        self._load_centers_grade()


    def _assign_willaya(self,willaya):
        print(willaya.willaya)




