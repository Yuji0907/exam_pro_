from sqlalchemy.orm import Session
from sqlalchemy import select

from database.orm_models import Candidate as CandidateORM
from database.orm_models import Code as CodeORM
from models.candidate_model import CandidateModel


class CandidateRepository:

    def __init__(self, session: Session):
        self.session = session

    # --------------------------------------------------
    # ORM -> Domain
    # --------------------------------------------------

    def _to_model(
        self,
        candidate: CandidateORM
    ) -> CandidateModel:

        return CandidateModel(
            file_number=candidate.file_number,
            first_name=candidate.first_name,
            last_name=candidate.last_name,
            willaya_id=candidate.willaya_id,
            # willaya_center_id=candidate.willaya_center_id
        )

    # --------------------------------------------------
    # Get all
    # --------------------------------------------------

    def get_all(self) -> list[CandidateModel]:

        candidates = (
            self.session
            .query(CandidateORM)
            .all()
        )

        return [
            self._to_model(candidate)
            for candidate in candidates
        ]

    # --------------------------------------------------
    # Get by file number
    # --------------------------------------------------

    def get_by_file_number(
        self,
        file_number: int
    ) -> CandidateModel | None:

        candidate = self.session.get(
            CandidateORM,
            file_number
        )

        if candidate is None:
            return None

        return self._to_model(candidate)
    
    def get_by_willaya(
        self,
        willaya_id: int
    ) -> list[CandidateModel] | None:

        candidates = self.session.scalars(
            select(CandidateORM).where(
                CandidateORM.willaya_id == willaya_id
            )
        ).all()

        if candidates is None:
            return []

        return [
            self._to_model(candidate)
            for candidate in candidates
        ]

    
    def get_by_barCode(
        self,
        bar_code: str
    ) -> CandidateModel | None:
        stm=(
            select(CandidateORM,CodeORM)
            .join(CodeORM,CandidateORM.file_number == CodeORM.file_number)
            .where(CodeORM.code == bar_code)
             )
        res=  self.session.execute(stm).all()

        return res
    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create(
        self,
        file_number: int,
        first_name: str,
        last_name: str,
        willaya_id: int | None = None
        
    ) -> tuple[CandidateModel, bool]:

        existing = self.get_by_file_number(file_number)

        if existing:
            return existing, True

        candidate = CandidateORM(
            file_number=file_number,
            grade = 0,
            first_name=first_name,
            last_name=last_name,
            willaya_id=willaya_id
        )

        self.session.add(candidate)
        self.session.commit()
        self.session.refresh(candidate)

        return self._to_model(candidate), False

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update(
        self,
        candidate: CandidateModel
    ) -> CandidateModel | None:

        existing = self.session.get(
            CandidateORM,
            candidate.file_number
        )

        if existing is None:
            return None

        existing.first_name = candidate.first_name
        existing.last_name = candidate.last_name
        existing.willaya_id = candidate.willaya_id

        self.session.commit()
        self.session.refresh(existing)

        return self._to_model(existing)

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(
        self,
        file_number: int
    ) -> bool:

        candidate = self.session.get(
            CandidateORM,
            file_number
        )

        if candidate is None:
            return False

        self.session.delete(candidate)
        self.session.commit()

        return True