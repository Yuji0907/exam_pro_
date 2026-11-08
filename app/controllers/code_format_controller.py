from sqlalchemy.orm import Session

from repositories.code_format_repo import CodeFormatRepository


class CodeFormatController:
    def __init__(self, view, session: Session):
        self.view = view
        self.session = session
        self.code_format_repo = CodeFormatRepository(session)

    # ---------------- combos ----------------

    def load_grades(self):
        self.view.load_grades(self.code_format_repo.get_grades())

    def load_centers(self, grade_id: int):
        self.view.load_centers(self.code_format_repo.get_centers_by_grade(grade_id))

    def load_subjects(self, grade_id: int):
        self.view.load_subjects(self.code_format_repo.get_subjects_by_grade(grade_id))

    # ---------------- code format ----------------

    def load_code_format(self, center_id: int, grade_id: int, subject_id: int):
        code_format = self.code_format_repo.get_by_ids(center_id, grade_id, subject_id)
        if code_format:
            self.view.display_code_format(code_format)
        else:
            self.view.show_error(
                f"No code format for center={center_id}, grade={grade_id}, subject={subject_id}"
            )

    def check_editable(self, center_id: int, grade_id: int, subject_id: int) -> bool:
        """False once codes have been generated from this format."""
        return not self.code_format_repo.has_codes(center_id, grade_id, subject_id)

    def assign_default(self):
        try:
            self.code_format_repo.ensure_defaults()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))

    # ---------------- uniqueness checks ----------------

    def check_center_format(self, center_format: str, center_id: int) -> bool:
        """True if free. The center code must not belong to another center."""
        if not center_format:
            return True
        rows = self.code_format_repo.get_by_center_format(center_format)
        return all(r.center_id == center_id for r in rows)

    def check_grade_format(self, grade_format: str, grade_id: int) -> bool:
        if not grade_format:
            return True
        rows = self.code_format_repo.get_by_grade_format(grade_format)
        return all(r.grade_id == grade_id for r in rows)

    # ---------------- save / delete ----------------

    def save_code_format(
        self,
        center_id: int,
        grade_id: int,
        subject_id: int,
        center_format: str,
        grade_format: str,
        subject_format: str,
        value_format: str,
    ):
        try:
            if not self.check_editable(center_id, grade_id, subject_id):
                self.view.show_error("codes already generated, format is locked")
                return
            if not self.check_center_format(center_format, center_id):
                self.view.show_error("le code center existe deja ...")
                return
            if not self.check_grade_format(grade_format, grade_id):
                self.view.show_error("le code grade existe deja ...")
                return

            self.code_format_repo.save(
                center_id, grade_id, subject_id,
                center_format, grade_format, subject_format, value_format,
            )
            # center and grade formats are shared by all their rows
            self.code_format_repo.set_center_format(center_id, center_format)
            self.code_format_repo.set_grade_format(grade_id, grade_format)

            self.session.commit()
            self.view.show_success("format saved")
        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))

    def delete_code_format(self, center_id: int, grade_id: int, subject_id: int):
        try:
            if not self.check_editable(center_id, grade_id, subject_id):
                self.view.show_error("codes already generated, cannot delete")
                return
            self.code_format_repo.delete(center_id, grade_id, subject_id)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))