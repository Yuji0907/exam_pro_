from dotenv import load_dotenv
from database.db_manager import DBManager
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
# from views.code_printing import CodePrint
from views.code_format_view import  CodeFormat as CodeFormatView
from views.code_printing_view import CodeGenerator
from views.evaluation_view import EvalView 
from views.assign_code_view import CodeAssignmentView 
from views.candidate_view import CandidateView
from views.subjects_view import SubjectsView
from views.center_view import CenterView
from views.main_window import MainWindow 
import os
load_dotenv()
database_connection_string = os.getenv("DB_CONNECTION_STRING")




if __name__ == "__main__":
    db = DBManager(database_connection_string)
    session = db.get_session()
    # db.create_all_tables()

    app = QApplication(sys.argv)



    
    # main_window_view = MainWindow(session=session)
    # main_window_view.show() 


    # code_format_view = CodeFormatView(session=session)
    # code_format_view.show() 
    # #    
    # codeGen_view = CodeGenerator(session)
    # codeGen_view.show()    

    # eval_view = EvalView(session)
    # eval_view.show()   
    
    # eval_view = EvalView(session)
    # eval_view.show()   
    #  
    # code_assignment = CodeAssignmentView(session)
    # code_assignment.show()    

    # candidate_view = CandidateView(session)
    # candidate_view.show()

    # subjects_view = SubjectsView(session)
    # subjects_view.show()

    center_view = CenterView(session)
    center_view.show()
    

    sys.exit(app.exec_())

print("finished")
