from sqlalchemy.orm import Session

from database.orm_models import Eval as EvalORM
from models.eval_model import EvalModel


class EvalRepository:

    def __init__(self, session: Session):
        self.session = session

    # ---------------------------------------------
    # ORM -> Domain
    # ---------------------------------------------

    def _to_model(
        self,
        evaluation: EvalORM
    ) -> EvalModel:

        return EvalModel(
            id=evaluation.id,
            code_id=evaluation.code_id,
            eval_value=evaluation.eval_value
        )

    # ---------------------------------------------
    # Get all
    # ---------------------------------------------

    def get_all(self) -> list[EvalModel]:

        evaluations = (
            self.session
            .query(EvalORM)
            .all()
        )

        return [
            self._to_model(evaluation)
            for evaluation in evaluations
        ]

    # ---------------------------------------------
    # Get by ID
    # ---------------------------------------------

    def get_by_id(
        self,
        eval_id: int
    ) -> EvalModel | None:

        evaluation = self.session.get(
            EvalORM,
            eval_id
        )

        if evaluation is None:
            return None

        return self._to_model(evaluation)

    # ---------------------------------------------
    # Get by code
    # ---------------------------------------------

    def get_by_code_id(
        self,
        code_id: int
    ) -> EvalModel | None:

        evaluation = (
            self.session
            .query(EvalORM)
            .filter(
                EvalORM.code_id == code_id
            )
            .first()
        )

        if evaluation is None:
            return None

        return self._to_model(evaluation)

    # ---------------------------------------------
    # Create
    # ---------------------------------------------

    def create(
        self,
        code_id: int,
        eval_value: float
    ) -> tuple[EvalModel, bool]:

        existing = self.get_by_code_id(code_id)

        if existing:
            return existing, True

        evaluation = EvalORM(
            code_id=code_id,
            eval_value=eval_value
        )

        self.session.add(evaluation)
        self.session.commit()
        self.session.refresh(evaluation)

        return self._to_model(evaluation), False

    # ---------------------------------------------
    # Update
    # ---------------------------------------------

    def update(
        self,
        evaluation: EvalModel
    ) -> EvalModel | None:

        existing = self.session.get(
            EvalORM,
            evaluation.id
        )

        if existing is None:
            return None

        existing.eval_value = evaluation.eval_value

        self.session.commit()
        self.session.refresh(existing)

        return self._to_model(existing)

    # ---------------------------------------------
    # Delete
    # ---------------------------------------------

    def delete(
        self,
        eval_id: int
    ) -> bool:

        evaluation = self.session.get(
            EvalORM,
            eval_id
        )

        if evaluation is None:
            return False

        self.session.delete(evaluation)
        self.session.commit()

        return True