from repositories.subject_repo import SubjectRepository
from sqlalchemy.orm import Session
from models.subject_model import SubjectModel


class SubjectController:

    def __init__(self, view, session: Session):
        self.view = view
        self.subject_repo = SubjectRepository(session)

    def load_subjects(self):
        subjects = self.subject_repo.get_all()
        self.view.load_subjects(subjects)

    def load_subject(self, subject_id: int):
        subject = self.subject_repo.get_by_id(subject_id)

        if subject:
            pass
        else:
            self.view.show_error(
                f"No wilaya found with id={subject_id}"
            )

    def create_subject(self, subject_id: int, subject: str, coeff: int):
        try:
            new_subject = self.subject_repo.create(
                subject_id,
                subject,
                coeff,
            )

            self.view.show_success(
                f"Subject created: {new_subject.subject}"
            )

            self.load_subjects()

        except Exception as e:
            self.view.show_error(str(e))

    def update_subject(
        self,
        subject: SubjectModel,
        name:str,
        coeff:int
    ):
        if name is not None:
            subject.subject = name
        if coeff is not None:
            subject.coeff = coeff


        try:
            updated = self.subject_repo.update(subject)
            if updated is None:
                self.view.show_error("Subject not found.")
                return

            self.view.show_success("Subject updated.")
            self.load_subjects()

        except Exception as e:
            self.view.show_error(str(e))

    def delete_subject(self, subject_id: int):
        try:
            deleted = self.subject_repo.delete(subject_id)
            if not deleted:
                self.view.show_error("Subject not found.")
                return

            self.view.show_success("Subject deleted.")
            self.load_subjects()

        except Exception as e:
            self.view.show_error(str(e))