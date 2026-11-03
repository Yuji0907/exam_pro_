

from repositories.code_format_repo import CodeFormatRepository
from repositories.code_repo import CodeRepository
from repositories.subject_repo import SubjectRepository
from repositories.willaya_repo import WillayaRepository
from sqlalchemy.orm import Session
from models.code_format_model import CodeFormat as CodeFormatModel

class CodeFormatController:
    def __init__(self, view, session:Session):
        self.view = view
        self.code_format_repo = CodeFormatRepository(session)
        self.subject_repo = SubjectRepository(session)
        self.willaya_repo = WillayaRepository (session)
        self.code_format_repo = CodeFormatRepository(session)
        self.code_repo = CodeRepository(session)


    def check_editable(self,code_format):
        res = self.code_repo.get_by_codeformat(code_format)
        return res



    def load_code_formats(self):
        code_formats = self.code_format_repo.get_all()
        self.view.display_code_formats(code_formats)

    def load_code_format(self,willaya_id: int,subject_id: int):
        code_format = self.code_format_repo.get_by_ids(willaya_id,subject_id)
        if code_format:
            self.view.display_code_format(code_format)
        else:
            self.view.show_error(f"No data found with id={willaya_id},{subject_id}")
    
    def assign_default(self):
        subjects= self.subject_repo.get_all()
        willays= self.willaya_repo.get_all()
        for wilaya in willays:
            for subject in subjects:
                self.create_code_format(
                    willaya_id=wilaya.id,
                    subject_id=subject.id,
                    willaya_format="",
                    subject_format="",
                    value_format=""
                )


    def check_exists(self,willaya_format,willaya_id):

        code_format = self.code_format_repo.get_by_willaya_format(willaya_format)
        if  len(code_format )==0:
            return
        
        if code_format[0].willaya_id == willaya_id:
            return
        self.view.on_willaya_format_error("le code willaya existe deja ...",)

    
    
    def create_code_format(self,
        willaya_id: int,
        subject_id: int,
        willaya_format: str,
        subject_format: str,
        value_format: str
    ):
        try:
            subjects= self.subject_repo.get_all()
            for subject in subjects: 
                if subject.id == subject_id:
                    new_code_format = self.code_format_repo.create(
                        willaya_id,subject_id,
                        willaya_format,subject_format,value_format
                    )
                else:
                    new_code_format = self.code_format_repo.create(
                        willaya_id,subject.id,
                        willaya_format,"",""
                    )
                self.view.show_success(f"User created: {new_code_format.value_format}")
                self.load_users()  # refresh the list
        except Exception as e:
            print(e)
            if str(e).startswith("CodeFormat already exists"):
                print("update")
                print(willaya_format)

                code_format = self.code_format_repo.get_by_ids(willaya_id=willaya_id,subject_id=subject_id)
                code_format.willaya_format=willaya_format
                code_format.subject_format=subject_format
                code_format.value_format=value_format
                self.code_format_repo.update(codeformat=code_format)
                

            # self.view.show_error(str(e))

    def update_code_format(
            self, code_format: CodeFormatModel,
            willaya_format:str,subject_format:str,value_format:str
    ):
        if subject_format is not None:
            code_format.subject_format =  subject_format         

        if willaya_format is not None:
            code_format.willaya_format =  subject_format    

        if value_format is not None:
            code_format.value_format =  subject_format       

        self.code_format_repo.update(code_format)

    def delete_code_format(self, willaya_id: int,subject_id: int,):
        self.code_format_repo.delete(willaya_id,subject_id)
        self.load_code_formats()  