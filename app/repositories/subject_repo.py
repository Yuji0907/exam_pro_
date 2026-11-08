from sqlalchemy.orm import Session
from sqlalchemy import select,func
from database.orm_models import Subject as SubjectORM
from database.orm_models import Subject_to_grade as  SubjectToGradeOrm
from database.orm_models import Grade as GradeOrm

from models.subject_grade_model import Subject_grade as Subject_grade_model
from models.grade_model import GradeModel
from models.subject_model import SubjectModel

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    # fetching
    def get_all(self)-> list[SubjectModel]:
        orm_res = self.session.query(SubjectORM).all()
        return [self._to_model(x) for x in orm_res]
    
    def get_all_subjects_grades(self)-> list[Subject_grade_model]:
        subjects_grades:list[Subject_grade_model]=[]
        subjects_grade:Subject_grade_model=None
        # orm_res = self.session.query(SubjectToGradeOrm).all()
        stm = (
            select( 
                SubjectToGradeOrm.grade_id,
                func.json_agg(
                    func.json_build_object(
                        "subject_id",SubjectToGradeOrm.Subject_id,
                        "coeff",SubjectToGradeOrm.coeff
                    )
                    )
                    .label("subject_ids"),
            )
            .group_by(SubjectToGradeOrm.grade_id)
        )
        rows = self.session.execute(stm).all()
        print(rows)
        return rows
        # prev:int
        # for item in orm_res:
        #     if not(item.grade_id == prev.grade_id):
        #         subjects_grade.
        #     print(item.grade_id)

        # return [self._to_model(x) for x in orm_res]

    def get_by_id(self,id:int)-> SubjectModel | None:
        orm_res =self.session.get(SubjectORM,(id))
        return self._to_model(orm_res) if orm_res else None
    
    def get_by_id_orm(self,id:int)-> SubjectORM | None:
        orm_res =self.session.get(SubjectORM,(id))
        return orm_res

    def get_by_subject(self,subject:str)->SubjectORM |  None:
        stmt = select(SubjectORM).where(SubjectORM.subject == subject)
        subject = self.session.scalars(stmt).first()
        return self._to_model(subject) if subject else None

    def assign_to_grade(
            self,
            subject_id:int,
            grade_id:int,
            coeff:int
    ) -> bool:
        subject_grade = SubjectToGradeOrm(
            Subject_id=subject_id,
            grade_id = grade_id,
            coeff=coeff
        )
        self.session.add(subject_grade)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            return False
            raise
        self.session.refresh(subject_grade)
        return True

        

    #create 
    def create(self,
            subject: str,
    ) -> SubjectModel:    
        existing = self.get_by_subject(subject=subject)
        if existing:
            raise ValueError(
                f"subject already exists for id={id}, "
            )
        
        subject_ =SubjectORM(subject=subject)
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

        )