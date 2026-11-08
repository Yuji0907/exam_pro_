from typing import Optional

from sqlalchemy import select, delete as sa_delete
from sqlalchemy.orm import Session

# Adjust these imports to match your project layout
from database.orm_models import Center as CenterORM
from database.orm_models import CenterAssignment as CenterAssignmentORM
from database.orm_models import Grade as GradeORM

from models.grade_model import GradeModel



class GradeRepository:
    def __init__(self, session: Session):
        self.session = session

    # --------------------------------------------------
    # ORM -> Model
    # --------------------------------------------------

    def _to_model(self, grade: GradeORM) -> GradeModel:
        return GradeModel(
            id=grade.id,
            name=grade.name,
        )

    # --------------------------------------------------
    # Internal (returns ORM, used for update/delete)
    # --------------------------------------------------

    def _get_orm(self, grade_id: int) -> Optional[GradeORM]:
        return self.session.get(GradeORM, grade_id)

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def add(self, name: str) -> GradeModel:
        exists= self.exists_by_name(name=name)
        if(exists):
            return self.get_by_name(name=name),exists
        grade = GradeORM(name=name) 
        self.session.add(grade)
        self.session.flush()  # populates grade.id without committing
        self.session.commit()
        return self._to_model(grade),False

    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    def get(self, grade_id: int) -> Optional[GradeModel]:
        grade = self._get_orm(grade_id)
        return self._to_model(grade) if grade else None

    def get_by_name(self, name: str) -> Optional[GradeModel]:
        stmt = select(GradeORM).where(GradeORM.name == name)
        grade = self.session.scalars(stmt).first()
        return self._to_model(grade) if grade else None

    def exists_by_name(self, name: str) -> bool:
        stmt = select(GradeORM.id).where(GradeORM.name == name).limit(1)
        return self.session.scalars(stmt).first() is not None

    def get_all(self) -> list[GradeModel]:
        stmt = select(GradeORM).order_by(GradeORM.name)
        grades = self.session.scalars(stmt).all()
        print("query ====")
        print(grades)
        return [self._to_model(grade) for grade in grades]

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def rename(self, grade_id: int, new_name: str) -> Optional[GradeModel]:
        grade = self._get_orm(grade_id)
        if grade is None:
            return None
        grade.name = new_name
        self.session.flush()
        return self._to_model(grade)

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(self, grade_id: int) -> bool:
        grade = self._get_orm(grade_id)
        if grade is None:
            return False
        self.session.delete(grade)
        self.session.flush()
        return True