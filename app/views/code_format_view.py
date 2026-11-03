from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QHeaderView,
    QAbstractItemView
)
from sqlalchemy.orm import Session
from controllers.code_format_controller import CodeFormatController
from controllers.willaya_controller import WillayaController
from controllers.subject_controller import SubjectController
from models.willaya_model import WillayaModel
from models.subject_model import SubjectModel 
from models.code_format_model import CodeFormat  as CodeFormatModel
from pathlib import Path


class CodeFormat(QWidget):
    def __init__(self,session:Session):
        super().__init__()
        self.wilaya_data:int =None
        self.subject_data:int = None
        self.subject_combo = QComboBox()
        self.wilaya_combo = QComboBox()
        self.table = QTableWidget(1, 3)
        self.setWindowTitle("code format")

        style_path = Path(__file__).parent.parent  / "styles" / "components.qss"
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)

        self.setObjectName("Container")



        self.code_format_controller = CodeFormatController(view=self,session=session)
        self.willaya_controller = WillayaController(view=self,session=session)
        self.subject_controller = SubjectController(view=self,session=session)
        # self.display_code_format()


        self.code_format_controller.load_code_formats()
        self.willaya_controller.load_willayas()
        self.subject_controller.load_subjects()

        self.setFixedSize(500,600)
        layout = QVBoxLayout()


        # Combos
  
        self.wilaya_combo.currentIndexChanged.connect(self.onWillayaChanged)
        self.subject_combo.currentIndexChanged.connect(self.onSubjectChanged)
        self.onSubjectChanged(0)

        #message8
        self.message = QLabel("")
        self.message.setObjectName("W_error")
        # self.message.setAlignment(Qt.AlignC)

        message_row = QHBoxLayout()
        message_row.addStretch()
        message_row.addWidget(self.message)
        message_row.addStretch()

        # Table
        self.table.setHorizontalHeaderLabels([
            "willaya",
            "subject",
            "Value"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellChanged.connect(self.on_cell_changed)

        # Button
        self.print_button = QPushButton("asssign format")
        self.print_button.setObjectName("Button")

        self.print_button.clicked.connect(self.generate_code)

        # Layout
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Wilaya"))
        combo_layout.addWidget(self.wilaya_combo)

        combo_layout.addWidget(QLabel("Subject"))
        combo_layout.addWidget(self.subject_combo)

        layout.addLayout(combo_layout)
        layout.addLayout(message_row)
        layout.addWidget(self.table)
        layout.addWidget(self.print_button)
        # layout.addStretch()

        self.setLayout(layout)

    def clear_message(self):
        self.message.setText("")

    def on_cell_changed(self,row,column):
        print(row,column)
        if not any((row,column)):
            print("check..")
            self.item = self.table.item(row,column)
            if self.item is not None:
                willaya = self.item.text()
                print(willaya)
                self.code_format_controller.check_exists(willaya_format=willaya,willaya_id=self.wilaya_data)


    def on_willaya_format_error(self,message):
        self.message.setText(str(message))
        self.item.setText("")

    def on_table_cell_error(self,message):
        self.message.setText(str(message))


    def load_willayas(self,willayas:list[WillayaModel]):
        for willaya in willayas :    
            print(type(willaya))
            self.wilaya_combo.addItem(willaya.willaya,willaya.id)
        self.wilaya_data= self.wilaya_combo.itemData(0)
        
    def load_subjects(self,subjects:list[SubjectModel]):
        for subject in subjects :    
            self.subject_combo.addItem(subject.subject,subject.id)
        self.subject_data=self.subject_combo.itemData(0)



    def get_table_items(self):
        parts = []
        for column in range(self.table.colorCount()):
            for row in range(self.table.rowCount()):
                if self.table.item(row, column) is not None:
                    value = self.table.item(row, column).text()
                    parts.append(value)
        return parts

    def generate_code(self):
        parts  = self.get_table_items()

        if(len(parts) <= 0):
            self.on_table_cell_error("code format cellules vide !")
            return
        
        self.code_format_controller.create_code_format(
            self.wilaya_data,
            self.subject_data,
            parts[0], 
            parts[1],
            parts[2],
            )
        code = " ".join(parts)

        print("Generated code:", code)



    def cleartable(self,):
        self.table.setRowCount(1)
        self.table.clearContents()
    def onSubjectChanged(self,index):
        self.cleartable()
        self.subject_data = self.subject_combo.itemData(index)
        self.code_format_controller.load_code_format(self.wilaya_data,self.subject_data)

    def onWillayaChanged(self,index):
        self.cleartable()
        self.wilaya_data = self.wilaya_combo.itemData(index)
        self.code_format_controller.load_code_format(self.wilaya_data,self.subject_data)




        


    def check_editable(self):
        parts = self.get_table_items()
        print(parts)
        if(len(parts) <= 0):
            return
        code = "".join(parts)
        res= self.code_format_controller.check_editable(code)
        if(len(res)>0):
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)




    def display_code_formats(self,code_formats):
        # self.code_format_controller.load_code_format()
        pass

    def display_code_format(self,code_format:CodeFormatModel):
        self.table.setRowCount(0)
        self.table.clearContents()
        self.table.insertRow(0)
        self.table.setItem(
                    0,
                    0,
                    QTableWidgetItem(str(code_format._willaya_format))
                )
        self.table.setItem(
                    0,
                    1,
                    QTableWidgetItem(str(code_format._subject_format))
                )
        self.table.setItem(
                    0,
                    2,
                    QTableWidgetItem(str(code_format._value_format))
                )
        # print(code_format.willaya_format)
        # print(code_format.subject_format)
        # print(code_format.value_format)
        self.check_editable()

        pass
    def show_error(self,error):
        print(error)
        pass