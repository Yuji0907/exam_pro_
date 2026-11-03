from sqlalchemy.orm import Session

from repositories.candidate_repo import CandidateRepository
from models.candidate_model import CandidateModel


class CandidateController:

    def __init__(
        self,
        view,
        session: Session
    ):
        self.view = view

        self.candidate_repo = CandidateRepository(
            session
        )

    # --------------------------------------------------
    # Load candidates
    # --------------------------------------------------

    def load_candidates(self):

        candidates = self.candidate_repo.get_all()

        self.view.display_candidates(
            candidates
        )

    # --------------------------------------------------
    # Load one candidate
    # --------------------------------------------------

    def load_candidate(
        self,
        file_number: int
    ):

        candidate = (
            self.candidate_repo
            .get_by_file_number(file_number)
        )

        if candidate is None:

            print(
                f"No candidate found with file number "
                f"{file_number}"
            )

            return

        self.view.display_candidate(
            candidate
        )

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create_candidate(
        self,
        file_number: int,
        first_name: str,
        last_name: str,
        willaya_id: int | None = None
    ):

        try:

            candidate, already_exists = (
                self.candidate_repo.create(
                    file_number=file_number,
                    first_name=first_name,
                    last_name=last_name,
                    willaya_id=willaya_id
                )
            )

            if already_exists:

                self.view.show_error(
                    f"Candidate already exists: "
                    f"{candidate.file_number}"
                )

                return

            self.view.show_success(
                f"Candidate created: "
                f"{candidate.file_number}"
            )

            self.load_candidates()

        except Exception as e:

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update_candidate(
        self,
        candidate: CandidateModel
    ):

        try:

            updated = (
                self.candidate_repo
                .update(candidate)
            )

            if updated is None:

                self.view.show_error(
                    "Candidate not found."
                )

                return

            self.view.show_success(
                "Candidate updated."
            )

            self.load_candidates()

        except Exception as e:

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete_candidate(
        self,
        file_number: int
    ):

        try:

            deleted = (
                self.candidate_repo
                .delete(file_number)
            )

            if not deleted:

                self.view.show_error(
                    "Candidate not found."
                )

                return

            self.view.show_success(
                "Candidate deleted."
            )

            self.load_candidates()

        except Exception as e:

            self.view.show_error(
                str(e)
            )