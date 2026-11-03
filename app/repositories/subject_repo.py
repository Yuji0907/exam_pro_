from sqlalchemy.orm import Session
from database.orm_models import Subject as SubjectORM
from models.subject_model import SubjectModel

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    # fetching
    def get_all(self)-> list[SubjectModel]:
        orm_res = self.session.query(SubjectORM).all()
        return [self._to_model(x) for x in orm_res]

    def get_by_id(self,id:int)-> SubjectModel | None:
        orm_res =self.session.get(SubjectORM,(id))
        return self._to_model(orm_res) if orm_res else None
    
    def get_by_id_orm(self,id:int)-> SubjectORM | None:
        orm_res =self.session.get(SubjectORM,(id))
        return orm_res

    def get_by_subject(self,subject:str)->SubjectORM |  None:
        orm_res = self.session.get(SubjectORM,(subject))
        return self._to_model(orm_res)


    #create 
    def create(self,
            id:int,
            subject: str,
            coeff: int
    ) -> SubjectModel:    
        existing = self.get_by_id_orm(id)
        if existing:
            raise ValueError(
                f"subject already exists for id={id}, "
            )
        
        subject_ =SubjectORM(id=id,subject=subject,coeff=coeff)
        self.session.add(subject_)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(subject_)
        return self._to_model(subject_)

    def update(self, subject: SubjectModel) -> SubjectModel | None:
        existing = self.get_by_id_orm(subject.id)
        if existing is None:
            return None

        existing.subject = subject.subject
        existing.coeff = subject.coeff
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(existing)
        return self._to_model(existing)

    def delete(self, subject_id: int) -> bool:
        existing = self.get_by_id_orm(subject_id)
        if existing is None:
            return False

        self.session.delete(existing)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return True
    
    def _to_model(self, orm_subject: SubjectORM) -> SubjectModel:
        return SubjectModel(
            orm_subject.id,
            orm_subject.subject,
            orm_subject.coeff,
        )