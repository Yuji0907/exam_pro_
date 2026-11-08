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
from controllers.center_controller import CenterController
from models.center_model import CenterModel
from models.willaya_model import WillayaModel
from models.grade_model import GradeModel
from dataclasses import dataclass
from models.center_view_model import Center_model
from models.willaya_model import WillayaModel
from models.center_assingment_model import Center_Assingn_model as Center_assingment_model

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

    



class CenterView(QSplitter):
    def __init__(self, session: Session):
        
        super().__init__(Qt.Horizontal)
        self._centers: dict[int, CenterModel] = {}
        self._editing_center_id: int | None = None
        self.controller = CenterController(view=self, session=session)
        self.willaya_controller = WillayaController(view=self, session=session)
        self.grade_controller = GradeController(view=self, session=session)
        self.center_controller = CenterController(view=self, session=session)

        self.setWindowTitle("Centers")
        self.setMinimumSize(640, 480)
        self._current_center_assingment = 0
        self._center_assignments:list[Center_assingment_model]=self.center_controller.load_assignments()




        # style_path = Path(__file__).parent.parent / "styles" / "style.qss"
        # with open(style_path, "r", encoding="utf-8") as style_file:
        #     self.setStyleSheet(style_file.read())

        self.resize(900, 500)




        
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

        centers_mainLayout = QVBoxLayout(center_view)
        centers_mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        center_container = QWidget()
        self.centers_layout = QVBoxLayout(center_container)
        self.centers_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # scroll area wrapping the container
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(center_container)

        self.setStyleSheet(f"""
            QSplitter::handle:horizontal {{
                background-color: {SEPARATOR};
                margin: 0 1px;
                width: 9px;
            }}
        """)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search..")
        centers_mainLayout.addWidget(search_input)
        centers_mainLayout.addWidget(scroll_area, 1)
        self.controller.load_centers()

        # center name input
        self.center_name = QLineEdit()
        self.center_name.setPlaceholderText("name..")
        centers_mainLayout.addWidget(self.center_name)

        add_button = QPushButton("add")
        add_button.setObjectName("CustomButton")
        add_button.clicked.connect(self._add_new_center) 
        centers_mainLayout.addWidget(add_button)

        return center_view


    def display_centers(self, centers: list[CenterModel]) -> None:
        print("display centers =======")
        clear_layout(self.centers_layout)
        self._centers = {center.id: center for center in centers}
        for index, center in enumerate(centers):
            item = Item(text =center.name,button = "add",
                        on_click=lambda x= center :self._add_center_grade(x))
            self.centers_layout.addWidget(item)

            print(center.id)
            print(center.name)


    def _add_new_center(self):
        print(self.center_name.text())
        if self.center_name.text() == "":
            QMessageBox.warning(
                self,
                "the center name is missing",
                "the center name is missing"

                )
            return 
        self.center_controller.create_center(name=self.center_name.text())
        

    def show_error(self,e):
        QMessageBox.warning(self,"error",e)

    # -------------------------------------------------------------------------------------------
    # center grade view
    # -------------------------------------------------------------------------------------------
    def _build_center_grade_view(self) -> QWidget:
        center_view = QFrame()
        main_layout = QVBoxLayout(center_view)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # scrollable list of centers for the selected grade
        centers_container = QWidget()
        self.centers_grade_layout = QVBoxLayout(centers_container)
        self.centers_grade_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # grades combo ================
        self.grade_combo = QComboBox()
        self.grade_combo.currentIndexChanged.connect(self.handle_grade_changed)
        self.grade_controller.load_grades()
        main_layout.addWidget(self.grade_combo)


        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidget(centers_container)
        main_layout.addWidget(scroll_area, 1)

        save_button = QPushButton("save")
        save_button.setObjectName("CustomButton")
        save_button.clicked.connect(self._save_centers_grade)
        main_layout.addWidget(save_button)

        return center_view
    
    def _get_current_center_assingment(self):
        if len(self._center_assignments) == 0:
            return Center_assingment_model()
        return self._center_assignments[self._current_center_assingment]

    def _save_centers_grade(self):
        centers_grade: Center_assingment_model = self._get_current_center_assingment()

        if not centers_grade.centers:
            QMessageBox.warning(
                self,
                "No centers",
                "Please add at least one center to this grade.",
            )
            return

        missing = [
            str(c.center)
            for c in centers_grade.centers
            if not c.willayas
        ]
        if missing:
            QMessageBox.warning(
                self,
                "Missing willayas",
                "Please assign at least one willaya to:\n- " + "\n- ".join(missing),
            )
            return

        self.center_controller.assign_centers(center_assignment=centers_grade)

    def _load_centers_grade(self):
        centers_grade:Center_assingment_model =self._get_current_center_assingment()
        print(centers_grade)
        for index,center in enumerate(centers_grade.centers):
            center_card = Grade_center_card(center=center,on_click=lambda :print("hello"))
            center_card.clicked.connect(lambda x=index,y=centers_grade:self._on_center_clicked(x,y))
            self.centers_grade_layout.addWidget(center_card)

    def _refresh(self,value):
        print("====================")
        print(value)
        centers_grade:Center_assingment_model =self._get_current_center_assingment()
        # centers_grade.centers = centers_grade.centers 

    def _on_center_clicked(self,index,centers_grade:Center_assingment_model):
        print("clicked")
        print(index)
        centers_grade.current_center = index
        print(centers_grade.current_center )





    def handle_grade_changed(self,index):
        clear_layout(self.centers_grade_layout)
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
        new_assingment.current_center_changed.connect(self._refresh)
        self._center_assignments.append(new_assingment)
        self._current_center_assingment = len(self._center_assignments)-1
        self._load_centers_grade()



    def _add_center_grade(self,center:Center_model):
        print(center)
        centers_grade:Center_assingment_model =self._get_current_center_assingment()


        new_center = Center_model(
            id=center.id,
            center=center.name,
            willayas=[]
            )
        print("adding sig")
        new_center.willayas_changed.connect(self._refresh)
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
        centers_grade: Center_assingment_model = self._get_current_center_assingment()

        willaya_data = self.sender().willayaData
        willaya_id = willaya_data["id"]


        already_assigned = any(
            w.id == willaya_id
            for center in centers_grade.centers
            for w in center.willayas
        )
        if already_assigned:
            return

        current_center = centers_grade.centers[centers_grade.current_center]
        current_center.willayas.append(
            WillayaModel(id=willaya_id, willaya=willaya_data["willaya"])
        )

        clear_layout(self.centers_grade_layout)
        self._load_centers_grade()


    def _assign_willaya(self,willaya):
        print(willaya.willaya)




