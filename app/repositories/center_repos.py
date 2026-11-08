from typing import Optional
 
from sqlalchemy import select,func, delete as sa_delete
from sqlalchemy.orm import Session
 
from database.orm_models import Grade as GradeORM 
from database.orm_models import Center as CenterORM
from database.orm_models import Willaya as WillayaORM
from database.orm_models import CenterAssignment as CenterAssignmentORM
 
from models.willaya_model import WillayaModel 
from models.center_model import CenterModel, CenterAssignmentModel
from models.center_assingment_model import Center_Assingn_model
from models.center_view_model import Center_model as CenterViewModel

 
 
# ======================================================
# Center
# ======================================================
 
class CenterRepository:
    def __init__(self, session: Session):
        self.session = session
 
    # --------------------------------------------------
    # ORM -> Model
    # --------------------------------------------------
 
    def _to_model(self, center: CenterORM) -> CenterModel:
        return CenterModel(
            id=center.id,
            name=center.name,
        )
 
    # --------------------------------------------------
    # Internal (returns ORM, used for update/delete)
    # --------------------------------------------------
 
    def _get_orm(self, center_id: int) -> Optional[CenterORM]:
        return self.session.get(CenterORM, center_id)
 
    # --------------------------------------------------
    # Create
    # --------------------------------------------------
    def add(self, name: str) -> tuple[CenterModel, bool]:
        """Returns (center, already_exists).
 
        If a center with this name exists, it is returned and nothing is
        inserted. Otherwise a new center is created.
        """
        existing = self.get_by_name(name)
        if existing is not None:
            return existing, True
 
        center = CenterORM(name=name)
        self.session.add(center)
        self.session.flush()  # populates center.id without committing
        return self._to_model(center), False
 
    def create(self, name: str) -> tuple[CenterModel, bool]:
        """Same as add(); kept so CenterController keeps working."""
        return self.add(name)
    # --------------------------------------------------
    # Read
    # --------------------------------------------------
 
    def get(self, center_id: int) -> Optional[CenterModel]:
        center = self._get_orm(center_id)
        return self._to_model(center) if center else None
 
    def get_by_name(self, name: str) -> Optional[CenterModel]:
        stmt = select(CenterORM).where(CenterORM.name == name)
        center = self.session.scalars(stmt).first()
        return self._to_model(center) if center else None
 
    def exists_by_name(self, name: str) -> bool:
        stmt = select(CenterORM.id).where(CenterORM.name == name).limit(1)
        return self.session.scalars(stmt).first() is not None
 
    def get_all(self) -> list[CenterModel]:
        stmt = select(CenterORM).order_by(CenterORM.name)
        centers = self.session.scalars(stmt).all()
        return [self._to_model(center) for center in centers]
 
    # --------------------------------------------------
    # Update
    # --------------------------------------------------
 
    def update(self, center_id: int, new_name: str) -> Optional[CenterModel]:
        center = self._get_orm(center_id)
        if center is None:
            return None
        center.name = new_name
        self.session.flush()
        return self._to_model(center)
 
    # --------------------------------------------------
    # Delete
    # --------------------------------------------------
 
    def delete(self, center_id: int) -> bool:
        center = self._get_orm(center_id)
        if center is None:
            return False
        self.session.delete(center)
        self.session.flush()
        return True
 
 
# ======================================================
# CenterAssignment  (composite PK: grade_id + willaya_id)
# ======================================================
 
class CenterAssignmentRepository:
    def __init__(self, session: Session):
        self.session = session
 
    # --------------------------------------------------
    # ORM -> Model
    # --------------------------------------------------
 
    def _to_model(self, assignment: CenterAssignmentORM) -> CenterAssignmentModel:
        return CenterAssignmentModel(
            grade_id=assignment.grade_id,
            willaya_id=assignment.willaya_id,
            center_id=assignment.center_id,
        )
 
    # --------------------------------------------------
    # Internal (returns ORM, used for update/delete)
    # --------------------------------------------------
 
    def _get_orm(
        self, grade_id: int, willaya_id: int
    ) -> Optional[CenterAssignmentORM]:
        return self.session.get(CenterAssignmentORM, (grade_id, willaya_id))
 
    # --------------------------------------------------
    # Create / Upsert
    # --------------------------------------------------
 
    def add(
        self, grade_id: int, willaya_id: int, center_id: int
    ) -> CenterAssignmentModel:
        assignment = CenterAssignmentORM(
            grade_id=grade_id,
            willaya_id=willaya_id,
            center_id=center_id,
        )
        self.session.add(assignment)
        self.session.flush()
        return self._to_model(assignment)
 
    def assign(
        self, grade_id: int, willaya_id: int, center_id: int
    ) -> CenterAssignmentModel:
        """Create the assignment, or move it to a different center if it exists."""
        existing = self._get_orm(grade_id, willaya_id)
        if existing is not None:
            existing.center_id = center_id
            self.session.flush()
            return self._to_model(existing)
        print("======================create")
        return self.add(grade_id, willaya_id, center_id)
 
    # --------------------------------------------------
    # Read
    # --------------------------------------------------
 
    def get(
        self, grade_id: int, willaya_id: int
    ) -> Optional[CenterAssignmentModel]:
        assignment = self._get_orm(grade_id, willaya_id)
        return self._to_model(assignment) if assignment else None
 
    def get_center_id(self, grade_id: int, willaya_id: int) -> Optional[int]:
        stmt = select(CenterAssignmentORM.center_id).where(
            CenterAssignmentORM.grade_id == grade_id,
            CenterAssignmentORM.willaya_id == willaya_id,
        )
        return self.session.scalars(stmt).first()
 
    def get_center(self, grade_id: int, willaya_id: int) -> Optional[CenterModel]:
        stmt = (
            select(CenterORM)
            .join(CenterAssignmentORM, CenterAssignmentORM.center_id == CenterORM.id)
            .where(
                CenterAssignmentORM.grade_id == grade_id,
                CenterAssignmentORM.willaya_id == willaya_id,
            )
        )
        center = self.session.scalars(stmt).first()
        if center is None:
            return None
        return CenterModel(id=center.id, name=center.name)
 
    def get_all(self) -> list[Center_Assingn_model]:
        stmt = (
            select(
                GradeORM.id.label("grade_id"),
                GradeORM.name.label("grade_name"),
                CenterORM.id.label("center_id"),
                CenterORM.name.label("center_name"),
                WillayaORM.id.label("willaya_id"),
                WillayaORM.willaya.label("willaya_name"),
            )
            .select_from(GradeORM)
            .outerjoin(
                CenterAssignmentORM,
                CenterAssignmentORM.grade_id == GradeORM.id,
            )
            .outerjoin(
                CenterORM,
                CenterORM.id == CenterAssignmentORM.center_id,
            )
            .outerjoin(
                WillayaORM,
                WillayaORM.id == CenterAssignmentORM.willaya_id,
            )
            .order_by(GradeORM.id, CenterORM.name, WillayaORM.willaya)
        )
        rows = self.session.execute(stmt).all()

        grades: dict[int, Center_Assingn_model] = {}
        centers: dict[tuple[int, int], CenterViewModel] = {}  # (grade_id, center_id)

        for row in rows:
            grade_model = grades.get(row.grade_id)
            if grade_model is None:
                grade_model = Center_Assingn_model(
                    id=row.grade_id,
                    grade=row.grade_name,
                    centers=[],
                    current_center=0,
                )
                grades[row.grade_id] = grade_model

            if row.center_id is None:  # grade with no assignment yet
                continue

            key = (row.grade_id, row.center_id)
            center_model = centers.get(key)
            if center_model is None:
                center_model = CenterViewModel(
                    id=row.center_id,
                    center=row.center_name,
                    willayas=[],
                )
                centers[key] = center_model
                grade_model.centers.append(center_model)

            if row.willaya_id is not None:
                center_model.willayas.append(WillayaModel(id=row.willaya_id,willaya=row.willaya_name))

        # default current_center to the first center of each grade
        for grade_model in grades.values():
            if grade_model.centers:
                grade_model._current_center = grade_model.centers[0].id

        return list(grades.values())
 
    def get_by_center(self, center_id: int) -> list[CenterAssignmentModel]:
        stmt = select(CenterAssignmentORM).where(
            CenterAssignmentORM.center_id == center_id
        )
        assignments = self.session.scalars(stmt).all()
        return [self._to_model(a) for a in assignments]
 
    def get_by_grade(self, grade_id: int) -> list[CenterAssignmentModel]:
        stmt = select(CenterAssignmentORM).where(
            CenterAssignmentORM.grade_id == grade_id
        )
        assignments = self.session.scalars(stmt).all()
        return [self._to_model(a) for a in assignments]
 
    def get_by_willaya(self, willaya_id: int) -> list[CenterAssignmentModel]:
        stmt = select(CenterAssignmentORM).where(
            CenterAssignmentORM.willaya_id == willaya_id
        )
        assignments = self.session.scalars(stmt).all()
        return [self._to_model(a) for a in assignments]
 
    # --------------------------------------------------
    # Update
    # --------------------------------------------------
 
    def move_to_center(
        self, grade_id: int, willaya_id: int, new_center_id: int
    ) -> Optional[CenterAssignmentModel]:
        assignment = self._get_orm(grade_id, willaya_id)
        if assignment is None:
            return None
        assignment.center_id = new_center_id
        self.session.flush()
        return self._to_model(assignment)
 
    def reassign_center(self, old_center_id: int, new_center_id: int) -> int:
        """Move every assignment from one center to another. Returns rows moved."""
        stmt = select(CenterAssignmentORM).where(
            CenterAssignmentORM.center_id == old_center_id
        )
        assignments = self.session.scalars(stmt).all()
        for a in assignments:
            a.center_id = new_center_id
        self.session.flush()
        return len(assignments)
 
    # --------------------------------------------------
    # Delete
    # --------------------------------------------------
 
    def delete(self, grade_id: int, willaya_id: int) -> bool:
        assignment = self._get_orm(grade_id, willaya_id)
        if assignment is None:
            return False
        self.session.delete(assignment)
        self.session.flush()
        return True
 
    def delete_by_center(self, center_id: int) -> int:
        stmt = sa_delete(CenterAssignmentORM).where(
            CenterAssignmentORM.center_id == center_id
        )
        result = self.session.execute(stmt)
        return result.rowcount
 