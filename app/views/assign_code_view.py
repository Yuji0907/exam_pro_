import code

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel,QTableWidget, QTableWidgetItem,QHBoxLayout,QFrame
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from components.CheckRow import CheckRow
from components.RoundedImage import RoundedImage
from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt
from utils.codeBar.CameraScanner import scanLoop
from PyQt5.QtGui import QIntValidator
from controllers.code_controller import CodeController
from controllers.assigning_controller import AssigningController

from pathlib import Path
class Worker(QThread):
    finished = pyqtSignal()
    code_detected = pyqtSignal(str)

    def run(self):
        scanLoop(self.code_detected)
        self.finished.emit()
class CodeAssignmentView(QFrame):

    def __init__(self,session ):
        super().__init__()
        self.codeController= CodeController(view=self,session=session)
        self.assignController = AssigningController(view=self,session=session)
        self.number_per_packet = 0
        style_path = Path(__file__).parent.parent  / "styles" / "components.qss"
        self.ERROR_STYLE ="""
                QLineEdit {
                    border:2px solid red;
                    font-size:16px;
                    border-radius:10px;
                    padding:10px;
                }
            """
        self.NOTICE_STYLE ="""
                QLineEdit {
                    border:2px solid orange;
                    font-size:16px;
                    border-radius:10px;
                    padding:10px;

                }
            """
        self.VALID_STYLE ="""
                QLineEdit {
                    border:2px solid green;
                    font-size:16px;
                    border-radius:10px;
                    padding:10px;
                }
            """
        self.DEFAULT_STYLE = """
                QLineEdit {
                    font-size:16px;
                    border-radius:10px;
                    padding:10px;
                    border:1px solid gray;
                }
            """
        with open(style_path, "r") as file: 
            style = file.read()
            self.setStyleSheet(style)
        self.setObjectName("Card")
        worker = Worker()
        worker.code_detected.connect(lambda res:self.Scaned(res))
        worker.start()

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,100)

        image = RoundedImage(
            "assets/scanBackground.png",
            radius=(0,25)
        )

        self.mainLayout.addWidget(image)


        # ==========================================
        # title
        # ==========================================

        self.title = QLabel("Affectation des codes-barres aux candidats")
        self.title.setObjectName("SideBarTitle")
        title_row = QHBoxLayout()
        # title_row.addStretch()
        title_row.addStretch()
        title_row.addWidget(self.title)
        title_row.addStretch()
        self.mainLayout.addLayout(title_row)

        # ==========================================
        # packets 
        # ==========================================
        packet_column = QVBoxLayout()
        packet_row_1 = QHBoxLayout()
        packet_row_2 = QHBoxLayout()
        packet_row_3 = QHBoxLayout()

        self.total_number =QLineEdit()
        self.total_number.setDisabled(True)
        
        self.total_number.setObjectName("Packets")
        self.total_lable = QLabel("nombre totale des candidats")
        self.total_lable.setObjectName("Link")
        self.total_number.setFixedSize(round(self.width()*.1), 20)


        packet_row_1.addStretch()
        packet_row_1.addStretch()
        packet_row_1.addStretch()
        packet_row_1.addStretch()
        packet_row_1.addWidget(self.total_lable)
        packet_row_1.addWidget(self.total_number)
        packet_row_1.addStretch()




        self.packet_count_lable = QLabel("nombre par lot")
        self.packet_count_lable.setObjectName("Link")
        self.packets_count =QLineEdit()
        self.packets_count.textChanged.connect(self.packet_number_validator) 
        self.packets_count.returnPressed.connect(self.set_number_per_packets) 
        self.packets_count.setObjectName("Packets")
        self.packets_count.setFixedSize(round(self.width()*.1), 20)

        packet_row_2.addStretch()
        packet_row_2.addStretch()
        packet_row_2.addStretch()
        packet_row_2.addStretch()
        packet_row_2.addWidget(self.packet_count_lable)
        packet_row_2.addWidget(self.packets_count)
        packet_row_2.addStretch()
        
        packet_column.addLayout(packet_row_1)
        packet_column.addLayout(packet_row_2)


        self.packet_number_lable = QLabel("nombres des lots creés")
        self.packet_number_lable.setObjectName("Link")
        self.packets_number =QLineEdit()
        self.packets_number.setObjectName("Packets")
        self.packets_number.setFixedSize(round(self.width()*.1), 20)

        packet_row_3.addStretch()
        packet_row_3.addStretch()
        packet_row_3.addStretch()
        packet_row_3.addStretch()
        packet_row_3.addWidget(self.packet_number_lable)
        packet_row_3.addWidget(self.packets_number)
        packet_row_3.addStretch()
        
        packet_column.addLayout(packet_row_1)
        packet_column.addLayout(packet_row_2)
        packet_column.addLayout(packet_row_3)



        
        self.mainLayout.addLayout(packet_column)



        # ==========================================
        # checks
        # ==========================================
        self.check1 = CheckRow("Scanner connecté")
        self.check1.check()
        self.check2 = CheckRow("lecture code bar")
        # self.check3 = CheckRow("Evaluation completed")
        self.check4 = CheckRow("Données enregistrées")
        self.packet_number = CheckRow("Numéro de paquet")




        self.mainLayout.addWidget(self.check1)
        self.mainLayout.addWidget(self.check2)
        # self.mainLayout.addWidget(self.check3)
        self.mainLayout.addWidget(self.check4)
        self.mainLayout.addWidget(self.packet_number)


        self.mainLayout.addStretch()    

        #--------------------
        # message
        #--------------------

        self.message = QLabel("")
        self.message.setObjectName("Message")
        self.message.setWordWrap(False)

        message_row = QHBoxLayout()
        # messagele_row.addStretch()
        message_row.addStretch()
        message_row.addWidget(self.message)
        message_row.addStretch()
        # message_row.addStretch()
        

        # ==========================================
        # input text 
        # =========================================


        self.input_field = QLineEdit()
        self.input_field.setStyleSheet(self.DEFAULT_STYLE)
        self.input_field.setFixedSize(round(self.width()*.2), 51)
        self.input_field.setDisabled(True)
        self.input_field.setPlaceholderText("enter candidates code")
        self.input_field.textChanged.connect(self.Grade_validator)

        self.name_field = QLineEdit()
        self.name_field.setStyleSheet(self.DEFAULT_STYLE)
        self.name_field.setFixedSize(round(self.width()*.5), 51)
        self.name_field.setDisabled(True)

        self.packet_field = QLineEdit()
        self.packet_field.setStyleSheet(self.DEFAULT_STYLE)
        self.packet_field.setFixedSize(round(self.width()*.3), 51)
        self.packet_field.setDisabled(True)


        input_row = QHBoxLayout()        
        input_row.addStretch()
        input_row.addWidget(self.input_field)
        input_row.addWidget(self.name_field)
        input_row.addWidget(self.packet_field)
        input_row.addStretch()
        input_row.addStretch()

        self.mainLayout.addStretch()
        self.mainLayout.addLayout(message_row)
        self.mainLayout.addLayout(input_row)


        # ==========================================
        # Done button
        # =========================================

        self.button = QPushButton("Affecter")
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
            value = int(text)
            # =================
            self.assignController.check_file_number_integrity(
                file_number=value,
                code_bar=self.eval_code
                )
        except ValueError:
            self.input_field.clear()
            return
        # if value > 9999999 or value <0  :
        #     self.input_field.backspace()
        #     self.input_field.setStyleSheet(self.ERROR_STYLE)
        # else:
        #     self.input_field.setStyleSheet(self.VALID_STYLE)
    def int_validator(self,text,text_input:QLineEdit,max)->bool:
        if not text:
            return False
        try:
            value = int(text)
        except ValueError:
            text_input.clear()
            return
        if  value <=0  :
            text_input.backspace()
            return False
            # text_input.setStyleSheet(self.ERROR_STYLE)
        else:
            return True
            pass
            # text_input.setStyleSheet(self.VALID_STYLE)     

    def setTotal(self,total):
        self.total = total
        self.total_number.setText(str(total))

    def packet_number_validator(self,text):
        
        valid =self.int_validator(text,
                    text_input=self.packets_count,
                    max=self.total_number)
        # self.total_number.setText(str(total))
        if(valid):
            self.number_per_packet = int(text)
            print("valid")
        else:
            print("not valid")

    def set_number_per_packets(self):
        # self.total_number.setText(str(total))
        print("preesed")
        if(self.number_per_packet<=0):
            return
        div = self.total // self.number_per_packet
        mod = self.total % self.number_per_packet
        print(f"pakets = {div} + papers= {mod}")
        packets = 0
        if(mod > 0 ): 
            packets = div+1
        else:
            packets = div
        
        self.packets_number.setText(str(packets))
        print(f"total packets = {packets}")
       
        self.input_field.setFocus()


    def display_candidate(self,candidate,old_codeBar,status,packet_name):
        print(candidate)
        self.edit_status = False
        if(candidate):
            print("------------")
            print(status)

            if(status=="edit"):
                print("edit ========")
                print(packet_name)
                # self.edit_status  = True
                self.message.setText("edit")
                self.packet_field.setText(packet_name)
                self.name_field.setText(f"{candidate.first_name} {candidate.last_name}")
                self.input_field.setText(f"{candidate.file_number}")
                self.input_field.setStyleSheet(self.NOTICE_STYLE)
                self.name_field.setStyleSheet(self.NOTICE_STYLE)
                self.packet_field.setStyleSheet(self.NOTICE_STYLE)

            elif (status == "forbiden"):
                self.message.setText("Numero dossier Déja affecter")
                self.input_field.setText(str(candidate.file_number))
                self.name_field.setText(f"{candidate.first_name} {candidate.last_name}==> {old_codeBar}")
                print("-------------")
                print(f"{packet_name}")
                self.packet_field.setText(f"{packet_name}")
                self.input_field.setStyleSheet(self.NOTICE_STYLE)
                self.name_field.setStyleSheet(self.NOTICE_STYLE)
                self.packet_field.setStyleSheet(self.NOTICE_STYLE)

            elif(status=="allowed"):
                self.message.setText("")
                self.name_field.setText(f"{candidate.first_name} {candidate.last_name}")
                self.input_field.setText(f"{candidate.file_number}")
                self.packet_field.setText(f"{packet_name}")
                self.input_field.setStyleSheet(self.VALID_STYLE)
                self.name_field.setStyleSheet(self.DEFAULT_STYLE)
                self.packet_field.setStyleSheet(self.DEFAULT_STYLE)


            elif(status=="willaya_error"):
                self.message.setText("willaya_error")
                self.name_field.setText(f"{candidate.first_name} {candidate.last_name}")
                self.input_field.setText(f"{candidate.file_number}")
                self.packet_field.setText(f"{packet_name}")
                self.input_field.setStyleSheet(self.NOTICE_STYLE)
                self.name_field.setStyleSheet(self.NOTICE_STYLE)

            else:
                print("sssssssssssssssssssssss")
                self.message.setText("")
                self.name_field.setText(f"")
                self.input_field.setText(f"")
                self.packet_field.setText(f"")
                self.input_field.setStyleSheet(self.VALID_STYLE)
                self.name_field.setStyleSheet(self.DEFAULT_STYLE)
        else:
            print("ssssssssss")
            self.message.setText("")
            self.name_field.setText(f"")                
            self.packet_field.setText(f"")

    def Scaned(self,res):
        # self.check3.checkOut()
        self.check4.checkOut()
        self.packet_number.checkOut()
        # self.hash_id.setText(res )
        self.button.setDisabled(False)
        self.input_field.setDisabled(False)
        self.input_field.setText("")
        self.eval_code=res
        self.check2.check(res)
        self.assignController.load_candidate_by_file_codeBar(res)
        self.assignController.load_candidates_total(res)

    def load_packet_info(self,pakets):
        print("packets ==========")
        self.packets_number.setText(str(len(pakets)))
        self.packets_count.setText(str(pakets[0].total_number))
        print(pakets)
    # def get_Packect_number(self):
    
    def evaluate(self):
        packets = int(self.packets_number.text())
        packet = self.assignController.create_packets(self.eval_code,packets,self.number_per_packet)
        # self.packet_field(packet.)
        self.check2.checkOut()
        # self.check3.check(self.input_field.text())
        file_number =int(self.input_field.text())
        packet_name = self.assignController.assign_packet(self.eval_code,file_number)
        self.packet_field.setText(packet_name)
        self.codeController.assign_code(self.eval_code,file_number)
        # backet_number = self.batchsController.get_batch_name(hash_id=self.candidate)
        self.check4.check(self.input_field.text())

        self.input_field.setDisabled(True)
        self.button.setDisabled(True)
        self.input_field.setStyleSheet(self.DEFAULT_STYLE)
