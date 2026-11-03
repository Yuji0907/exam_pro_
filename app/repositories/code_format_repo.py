
from sqlalchemy.orm import Session
from sqlalchemy import select ,and_
from database.orm_models import CodeFormat as CodeFormatORM
from database.orm_models import Code as CodeORM
from models.code_format_model import CodeFormat as CodeFormatModel


class CodeFormatRepository:
    def __init__(self, session: Session):
        self.session = session

    

    def get_all(self) -> list[CodeFormatModel]:
        orm_res = self.session.query(CodeFormatORM).all()
        return [self._to_model(x) for x in orm_res] 

    def get_by_ids(self, willaya_id: int, subject_id: int) -> CodeFormatModel | None:
        orm_res =self.session.get(CodeFormatORM, (willaya_id, subject_id))
        return self._to_model(orm_res) if orm_res else None
    
    def get_by_ids_orm(self, willaya_id: int, subject_id: int) -> CodeFormatORM | None:
        orm_res =self.session.get(CodeFormatORM, (willaya_id, subject_id))
        return orm_res

    def get_by_willaya(self, willaya_id: int) -> list[CodeFormatORM]:
        orm_res = self.session.query(CodeFormatORM).filter_by(willaya_id=willaya_id).all()
        return [self._to_model(x) for x in orm_res] 

    def get_by_willaya_format(self,willaya_format:str)->list[CodeFormatORM]:
        orm_res = self.session.query(CodeFormatORM).filter_by(willaya_format = willaya_format).all()
        return [self._to_model(x) for x in orm_res] 


    def get_by_subject(self, subject_id: int) -> list[CodeFormatORM]:
        orm_res = self.session.query(CodeFormatORM).filter_by(subject_id=subject_id).all()
        return [self._to_model(x) for x in orm_res] 

    def get_by_code_bar(self,code_bar)->CodeFormatORM:
        stm=(
            select(CodeORM,CodeFormatORM)
            .join(CodeORM,and_( CodeFormatORM.subject_id == CodeORM.format_subject_id,
                               CodeFormatORM.willaya_id == CodeORM.format_willaya_id)
                  )
            .where(CodeORM.code == code_bar)
             )
        res=  self.session.execute(stm).all()
        print("-----------------")
        # print(res)
        for code, codeFormat in res:
            print(codeFormat.subject_id)
            return codeFormat
        



    def create(
        self,
        willaya_id: int,
        subject_id: int,
        willaya_format: str,
        subject_format: str,
        value_format: str,
    ) -> CodeFormatModel:
        existing = self.get_by_ids(willaya_id, subject_id)
        if existing:
            raise ValueError(
                f"CodeFormat already exists for willaya_id={willaya_id}, "
                f"subject_id={subject_id}"
            )
        # self.update()
            # return self._to_model(existing)

        orm_code_format = CodeFormatORM(
            willaya_id=willaya_id,
            subject_id=subject_id,
            willaya_format=willaya_format,
            subject_format=subject_format,
            value_format=value_format,
        )
        self.session.add(orm_code_format)
        self.session.commit()
        self.session.refresh(orm_code_format)
        return self._to_model(orm_code_format)

    def update(
        self,codeformat : CodeFormatModel ) -> CodeFormatModel:
        orm_code_format = self.get_by_ids_orm(codeformat.willaya_id,codeformat.subject_id)
        print("===================")
        print(orm_code_format.subject_format)
        if not orm_code_format:
            raise ValueError(
                f"No CodeFormat found for willaya_id={codeformat.willaya_id}, "
                f"subject_id={codeformat.subject_id}"
            )

        orm_code_format.willaya_format = codeformat.willaya_format
        orm_code_format.subject_format = codeformat.subject_format
        orm_code_format.value_format = codeformat.value_format
        print(codeformat.value_format)
        print(orm_code_format.value_format)
        
        self.session.commit()
        self.session.refresh(orm_code_format)
        return self._to_model(orm_code_format)


    def delete(self, willaya_id: int, subject_id: int) -> None:
        orm_code_format = self.get_by_ids(willaya_id, subject_id)
        if orm_code_format:
            self.session.delete(orm_code_format)
            self.session.commit()


    def _to_model(self, orm_code_format: CodeFormatORM) -> CodeFormatModel:
        return CodeFormatModel(
            orm_code_format.willaya_id,
            orm_code_format.subject_id,
            orm_code_format.willaya_format,
            orm_code_format.subject_format,
            orm_code_format.value_format,
        )