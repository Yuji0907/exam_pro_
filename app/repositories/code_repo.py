from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.orm_models import Code as CodeORM
from database.orm_models import Center as CenterORM
from database.orm_models import Grade as GradeORM
from database.orm_models import Subject as SubjectORM
from models.code_model import CodeModel


class CodeRepository:
    """Repository methods only flush; the controller commits."""

    def __init__(self, session: Session):
        self.session = session

    # ---------------- ORM -> Model ----------------

    def _to_model(self, code: CodeORM) -> CodeModel:
        return CodeModel(
            id=code.id,
            code=code.code,
            format_center_id=code.format_center_id,
            format_grade_id=code.format_grade_id,
            format_subject_id=code.format_subject_id,
            reg_number=code.reg_number,
            candidate_grade_id=code.candidate_grade_id,
            packet_number=code.packet_number,
        )

    def get_by_id_orm(self, code_id: int) -> Optional[CodeORM]:
        return self.session.get(CodeORM, code_id)

    # ---------------- Read ----------------

    def get_all(self) -> list[CodeModel]:
        rows = self.session.scalars(select(CodeORM)).all()
        return [self._to_model(r) for r in rows]

    def get_by_id(self, code_id: int) -> Optional[CodeModel]:
        code = self.get_by_id_orm(code_id)
        return self._to_model(code) if code else None

    def get_by_code(self, code: str) -> Optional[CodeModel]:
        stmt = select(CodeORM).where(CodeORM.code == code)
        result = self.session.scalars(stmt).first()
        return self._to_model(result) if result else None

    def get_by_candidate(self, reg_number: int, grade_id: int) -> list[CodeModel]:
        stmt = select(CodeORM).where(
            CodeORM.reg_number == reg_number,
            CodeORM.candidate_grade_id == grade_id,
        )
        return [self._to_model(r) for r in self.session.scalars(stmt).all()]

    def get_by_format(
        self, center_id: int, grade_id: int, subject_id: int
    ) -> list[CodeModel]:
        """Replaces get_by_codeformat(): the format is now identified by ids."""
        stmt = select(CodeORM).where(
            CodeORM.format_center_id == center_id,
            CodeORM.format_grade_id == grade_id,
            CodeORM.format_subject_id == subject_id,
        )
        return [self._to_model(r) for r in self.session.scalars(stmt).all()]

    def existing_codes(self, codes: list[str]) -> list[str]:
        """Which of these code strings are already in the database."""
        if not codes:
            return []
        stmt = select(CodeORM.code).where(CodeORM.code.in_(codes))
        return list(self.session.scalars(stmt).all())

    def get_format_labels(
        self, center_id: int, grade_id: int, subject_id: int
    ) -> tuple[str, str, str]:
        """(center name, grade name, subject name), used for folder names."""
        center = self.session.get(CenterORM, center_id)
        grade = self.session.get(GradeORM, grade_id)
        subject = self.session.get(SubjectORM, subject_id)
        return center.name, grade.name, subject.subject

    # ---------------- Create ----------------

    def create(
        self,
        code: str,
        format_center_id: int,
        format_grade_id: int,
        format_subject_id: int,
    ) -> tuple[CodeModel, bool]:
        existing = self.get_by_code(code)
        if existing:
            return existing, True

        code_orm = CodeORM(
            code=code,
            format_center_id=format_center_id,
            format_grade_id=format_grade_id,
            format_subject_id=format_subject_id,
        )
        self.session.add(code_orm)
        self.session.flush()
        return self._to_model(code_orm), False

    def create_many(
        self,
        codes: list[str],
        format_center_id: int,
        format_grade_id: int,
        format_subject_id: int,
    ) -> list[CodeModel]:
        objects = [
            CodeORM(
                code=code,
                format_center_id=format_center_id,
                format_grade_id=format_grade_id,
                format_subject_id=format_subject_id,
            )
            for code in codes
        ]
        self.session.add_all(objects)
        self.session.flush()  # populates the ids
        return [self._to_model(o) for o in objects]

    # ---------------- Update ----------------

    def assign_to_candidate(
        self, code: str, reg_number: int, grade_id: int
    ) -> Optional[CodeModel]:
        stmt = select(CodeORM).where(CodeORM.code == code)
        code_orm = self.session.scalars(stmt).first()
        if code_orm is None:
            return None
        code_orm.reg_number = reg_number
        code_orm.candidate_grade_id = grade_id
        self.session.flush()
        return self._to_model(code_orm)

    def update(self, code: CodeModel) -> CodeModel:
        orm_code = self.get_by_id_orm(code.id)
        if orm_code is None:
            raise ValueError(f"No code found for id={code.id}")

        orm_code.code = code.code
        orm_code.reg_number = code.reg_number
        orm_code.candidate_grade_id = code.candidate_grade_id
        orm_code.format_center_id = code.format_center_id
        orm_code.format_grade_id = code.format_grade_id
        orm_code.format_subject_id = code.format_subject_id
        orm_code.packet_number = code.packet_number
        self.session.flush()
        return self._to_model(orm_code)

    # ---------------- Delete ----------------

    def delete(self, code: str) -> bool:
        stmt = select(CodeORM).where(CodeORM.code == code)
        code_orm = self.session.scalars(stmt).first()
        if code_orm is None:
            return False
        self.session.delete(code_orm)
        self.session.flush()
        return True