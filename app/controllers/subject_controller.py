from repositories.subject_repo import SubjectRepository
from repositories.grade_repo import GradeRepository
from sqlalchemy.orm import Session
from models.subject_model import SubjectModel
from models.grade_model import GradeModel
from models.subject_grade_model import Subject_grade 


class SubjectController:

    def __init__(self, view, session: Session):
        self.view = view
        self.subject_repo = SubjectRepository(session)
        self.grade_repo = GradeRepository(session)

    def load_subjects(self):
        subjects = self.subject_repo.get_all()
        self.view.load_subjects(subjects)

    def load_grades_subjects(self):
        subjects_grades:list[Subject_grade]=[]

        res = self.subject_repo.get_all_subjects_grades()
        print(res)
        for  item in res :
            subjects_grade:Subject_grade = Subject_grade()
            subjects_grade.id = item[0]
            subjects_grade.grade = self.grade_repo.get(item[0])
            for subject in item[1]:
                current_subject =self.subject_repo.get_by_id(subject["subject_id"])
                current_subject.coeff = subject["coeff"]
                subjects_grade.subjects.append(current_subject)
            subjects_grades.append(subjects_grade)
        return subjects_grades

    def load_subject(self, subject_id: int):
        subject = self.subject_repo.get_by_id(subject_id)

        if subject:
            pass
        else:
            self.view.show_error(
                f"No wilaya found with id={subject_id}"
            )

    def create_subject(self,subject: str):
        try:
            new_subject = self.subject_repo.create(
                subject
            )



            self.load_subjects()

        except Exception as e:
            raise(e)
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

    # -----------------
    # cross controller subjects grade
    # -----------------
    def _assign_subjects_to_grade(self,subject_grade:Subject_grade):
        grade_id = subject_grade.grade.id
        subjects= subject_grade.subjects
        try:
            for subject in subjects:
                self.subject_repo.assign_to_grade(
                    subject_id=subject.id,
                    grade_id=grade_id,
                    coeff=subject.coeff
                    )

        except Exception as e:
            self.view.show_error(str(e))
