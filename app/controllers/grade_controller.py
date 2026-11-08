from sqlalchemy.orm import Session
 
from repositories.grade_repo import GradeRepository
from models.grade_model import GradeModel
 
 
class GradeController:
 
    def __init__(self, view, session: Session):
        self.view = view
        self.session = session
        self.grade_repo = GradeRepository(session)
 
    def load_grades(self):
        grades = self.grade_repo.get_all()
        print("grades========")
        print(grades)
        self.view.load_grades(grades)
 
    def get_grades(self):
        return self.grade_repo.get_all()
 
    def load_grade(self, grade_id: int):
        grade = self.grade_repo.get(grade_id)
 
        if grade:
            self.view.display_grade(grade)
        else:
            self.view.show_error(
                f"No grade found with id={grade_id}"
            )
 
    def create_grade(self, name: str):
        try:
            name = name.strip()
 
            if not name:
                self.view.show_error("Grade name cannot be empty.")
                return
 
            grade, already_exists = self.grade_repo.add(name)
 
            if already_exists:
                self.view.show_error(
                    f"Grade already exists: {grade.name}"
                )
                return
 
            self.session.commit()
 

 
            self.load_grades()
 
        except Exception as e:
            self.session.rollback()
            # raise(e)
            self.view.show_error(str(e))
 
    def update_grade(
        self,
        grade: GradeModel,
        name: str | None = None
    ):
        if name is not None:
            grade.name = name
 
        try:
            updated = self.grade_repo.update(grade)
 
            if updated is None:
                self.view.show_error("Grade not found.")
                return
 
            self.session.commit()
 
            self.view.show_success("Grade updated.")
 
            self.load_grades()
 
        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))
 
    def delete_grade(self, grade_id: int):
        try:
            deleted = self.grade_repo.delete(grade_id)
 
            if not deleted:
                self.view.show_error("Grade not found.")
                return
 
            self.session.commit()
 
            self.view.show_success("Grade deleted.")
 
            self.load_grades()
 
        except Exception as e:
            # Fails if candidates, assignments, code formats or
            # subject links still reference this grade
            self.session.rollback()
            self.view.show_error(str(e))
 