from sqlalchemy.orm import Session

from repositories.code_repo import CodeRepository
from repositories.candidate_repo import CandidateRepository 
from repositories.eval_repo import EvalRepository
from models.code_model import CodeModel
from models.candidate_model import CandidateModel 

class EvalController:

    def __init__(
        self,
        view,
        session: Session
    ):
        self.view = view

        self.code_repo = CodeRepository(
            session
        )
        self.candidateRepo = CandidateRepository(
            session
        )

        self.eval_repo = EvalRepository(
            session
        )



    def scan_code (
        self,
        code: str
    )->CandidateModel:

        code = code.strip()

        if not code:
            self.view.show_error(
                "Empty code."
            )
            return



        code_model = self.code_repo.get_by_code(
            code
        )

        if code_model is None:

            self.view.show_error(
                f"Unknown code: {code}"
            )

            return

        # -----------------------------------------
        # Code found
        # -----------------------------------------
        scaned_candidate = self.candidateRepo.get_by_file_number(code_model.file_number)
        return scaned_candidate

    # =============================================
    # Save evaluation
    # =============================================

    def evaluate(
        self,
        eval_code: str,
        grade: float
    ):

        # -----------------------------------------
        # Validate grade
        # -----------------------------------------

        if grade < 0 or grade > 20:

            self.view.show_error(
                "Grade must be between 0 and 20."
            )

            return

        # -----------------------------------------
        # Make sure code exists
        # -----------------------------------------

        code = self.code_repo.get_by_code(
            code=eval_code
        )

        if code is None:

            print(
                "Code not found."
            )

            return

        # -----------------------------------------
        # Prevent duplicate evaluation
        # -----------------------------------------

        existing = (
            self.eval_repo
            .get_by_code_id(
                code.id
            )
        )

        if existing is not None:

            print(
                "This code has already been evaluated."
            )

            return

        # -----------------------------------------
        # Save
        # -----------------------------------------

        try:

            evaluation, already_exists = (
                self.eval_repo.create(
                    code_id=code.id,
                    eval_value=grade
                )
            )

            if already_exists:

                print(
                    "This code has already been evaluated."
                )

                return

            # self.view.evaluation_saved(
            #     evaluation
            # )
            print("saved")
        except Exception as e:
            print(str(e))