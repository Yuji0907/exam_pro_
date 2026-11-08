from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from database.orm_models import CodeFormat as CodeFormatORM
from database.orm_models import CenterAssignment as CenterAssignmentORM
from database.orm_models import Center as CenterORM
from database.orm_models import Grade as GradeORM
from database.orm_models import Subject as SubjectORM
from database.orm_models import Subject_to_grade as SubjectToGradeORM
from database.orm_models import Code as CodeORM

from models.code_format_model import CodeFormat as CodeFormatModel


class CodeFormatRepository:
    def __init__(self, session: Session):
        self.session = session

    # ---------------- ORM -> Model ----------------

    def _to_model(self, cf: CodeFormatORM) -> CodeFormatModel:
        return CodeFormatModel(
            center_id=cf.center_id,
            grade_id=cf.grade_id,
            subject_id=cf.subject_id,
            center_format=cf.center_format,
            grade_format=cf.grade_format,
            subject_format=cf.subject_format,
            value_format=cf.value_format,
        )

    def _get_orm(self, center_id: int, grade_id: int, subject_id: int):
        # session.get expects the PK in column order: center, subject, grade
        return self.session.get(CodeFormatORM, (center_id, subject_id, grade_id))

    # ---------------- Read ----------------

    def get_by_ids(
        self, center_id: int, grade_id: int, subject_id: int
    ) -> Optional[CodeFormatModel]:
        cf = self._get_orm(center_id, grade_id, subject_id)
        return self._to_model(cf) if cf else None

    def get_all(self) -> list[CodeFormatModel]:
        rows = self.session.scalars(select(CodeFormatORM)).all()
        return [self._to_model(r) for r in rows]

    def get_by_center_format(self, center_format: str) -> list[CodeFormatModel]:
        stmt = select(CodeFormatORM).where(CodeFormatORM.center_format == center_format)
        return [self._to_model(r) for r in self.session.scalars(stmt).all()]

    def get_by_grade_format(self, grade_format: str) -> list[CodeFormatModel]:
        stmt = select(CodeFormatORM).where(CodeFormatORM.grade_format == grade_format)
        return [self._to_model(r) for r in self.session.scalars(stmt).all()]

    def has_codes(self, center_id: int, grade_id: int, subject_id: int) -> bool:
        stmt = (
            select(CodeORM.id)
            .where(
                CodeORM.format_center_id == center_id,
                CodeORM.format_grade_id == grade_id,
                CodeORM.format_subject_id == subject_id,
            )
            .limit(1)
        )
        return self.session.scalars(stmt).first() is not None

    # ---------------- Lookups for the combos (id, label) ----------------

    def get_grades(self) -> list[tuple[int, str]]:
        stmt = select(GradeORM.id, GradeORM.name).order_by(GradeORM.id)
        return [(r.id, r.name) for r in self.session.execute(stmt)]

    def get_centers_by_grade(self, grade_id: int) -> list[tuple[int, str]]:
        stmt = (
            select(CenterORM.id, CenterORM.name)
            .join(CenterAssignmentORM, CenterAssignmentORM.center_id == CenterORM.id)
            .where(CenterAssignmentORM.grade_id == grade_id)
            .distinct()
            .order_by(CenterORM.name)
        )
        return [(r.id, r.name) for r in self.session.execute(stmt)]

    def get_subjects_by_grade(self, grade_id: int) -> list[tuple[int, str]]:
        stmt = (
            select(SubjectORM.id, SubjectORM.subject)
            .join(SubjectToGradeORM, SubjectToGradeORM.Subject_id == SubjectORM.id)
            .where(SubjectToGradeORM.grade_id == grade_id)
            .order_by(SubjectORM.subject)
        )
        return [(r.id, r.subject) for r in self.session.execute(stmt)]

    # ---------------- Write ----------------

    def save(
        self,
        center_id: int,
        grade_id: int,
        subject_id: int,
        center_format: str,
        grade_format: str,
        subject_format: str,
        value_format: str,
    ) -> CodeFormatModel:
        """Insert or update the row for (center, grade, subject)."""
        cf = self._get_orm(center_id, grade_id, subject_id)
        if cf is None:
            cf = CodeFormatORM(
                center_id=center_id, grade_id=grade_id, subject_id=subject_id
            )
            self.session.add(cf)
        cf.center_format = center_format
        cf.grade_format = grade_format
        cf.subject_format = subject_format
        cf.value_format = value_format
        self.session.flush()
        return self._to_model(cf)

    def set_center_format(self, center_id: int, center_format: str) -> None:
        self.session.execute(
            update(CodeFormatORM)
            .where(CodeFormatORM.center_id == center_id)
            .values(center_format=center_format)
        )

    def set_grade_format(self, grade_id: int, grade_format: str) -> None:
        self.session.execute(
            update(CodeFormatORM)
            .where(CodeFormatORM.grade_id == grade_id)
            .values(grade_format=grade_format)
        )

    def _known_format(self, column, condition) -> str:
        stmt = select(column).where(condition, column != "").limit(1)
        return self.session.scalars(stmt).first() or ""

    def ensure_defaults(self) -> int:
        """Create an empty row for every (center, grade, subject) that has none.

        Pairs come from center_assignment, subjects from subject_to_grade.
        Returns the number of rows created.
        """
        pairs = self.session.execute(
            select(CenterAssignmentORM.grade_id, CenterAssignmentORM.center_id).distinct()
        ).all()

        created = 0
        for grade_id, center_id in pairs:
            subject_ids = self.session.scalars(
                select(SubjectToGradeORM.Subject_id).where(
                    SubjectToGradeORM.grade_id == grade_id
                )
            ).all()
            for subject_id in subject_ids:
                if self._get_orm(center_id, grade_id, subject_id) is not None:
                    continue
                self.session.add(
                    CodeFormatORM(
                        center_id=center_id,
                        grade_id=grade_id,
                        subject_id=subject_id,
                        center_format=self._known_format(
                            CodeFormatORM.center_format,
                            CodeFormatORM.center_id == center_id,
                        ),
                        grade_format=self._known_format(
                            CodeFormatORM.grade_format,
                            CodeFormatORM.grade_id == grade_id,
                        ),
                        subject_format="",
                        value_format="",
                    )
                )
                created += 1
        self.session.flush()
        return created

    def delete(self, center_id: int, grade_id: int, subject_id: int) -> bool:
        cf = self._get_orm(center_id, grade_id, subject_id)
        if cf is None:
            return False
        self.session.delete(cf)
        self.session.flush()
        return True