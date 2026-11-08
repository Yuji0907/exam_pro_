import os

from sqlalchemy.orm import Session

from utils.Barcode_gen import generate_barcode
from repositories.code_repo import CodeRepository
from repositories.code_format_repo import CodeFormatRepository


class CodeController:
    def __init__(self, view, session: Session):
        self.view = view
        self.session = session
        self.code_repo = CodeRepository(session)
        self.code_format_repo = CodeFormatRepository(session)

    # ---------------- combos ----------------

    def load_grades(self):
        self.view.load_grades(self.code_format_repo.get_grades())

    def load_centers(self, grade_id: int):
        self.view.load_centers(self.code_format_repo.get_centers_by_grade(grade_id))

    def load_subjects(self, grade_id: int):
        self.view.load_subjects(self.code_format_repo.get_subjects_by_grade(grade_id))

    # ---------------- load ----------------

    def load_codes(self):
        self.view.display_codes(self.code_repo.get_all())

    def load_candidate_codes(self, reg_number: int, grade_id: int):
        self.view.display_codes(self.code_repo.get_by_candidate(reg_number, grade_id))

    # ---------------- generate ----------------

    def generate_codes(
        self, center_id: int, grade_id: int, subject_id: int, quantity: int
    ):
        if quantity <= 0:
            self.view.show_error("Quantity must be greater than zero.")
            return

        try:
            code_format = self.code_format_repo.get_by_ids(
                center_id, grade_id, subject_id
            )
            if code_format is None:
                self.view.show_error(
                    "No code format exists for this center, grade and subject."
                )
                return

            start_string = code_format.value_format
            try:
                start = int(start_string)
            except ValueError:
                self.view.show_error(f"Invalid starting value: {start_string}")
                return

            width = len(start_string)
            prefix = (
                f"{code_format.center_format}"
                f"{code_format.grade_format}"
                f"{code_format.subject_format}"
            )
            values = [str(start + i).zfill(width) for i in range(quantity)]
            generated = [prefix + v for v in values]

            duplicates = self.code_repo.existing_codes(generated)
            if duplicates:
                self.view.show_error(
                    f"{len(duplicates)} codes already exist (first: {duplicates[0]})."
                )
                return

            # save the codes and move the format's counter to the next value
            codes = self.code_repo.create_many(
                generated, center_id, grade_id, subject_id
            )
            self.code_format_repo.save(
                center_id, grade_id, subject_id,
                code_format.center_format,
                code_format.grade_format,
                code_format.subject_format,
                str(start + quantity).zfill(width),
            )

            # barcodes: if this fails, the database changes are rolled back
            center_name, grade_name, subject_name = self.code_repo.get_format_labels(
                center_id, grade_id, subject_id
            )
            folder = os.path.join("temp")
            os.makedirs(folder, exist_ok=True)
            for code, value in zip(generated, values):
                generate_barcode(code, os.path.join(folder, value))

            self.session.commit()
            self.view.display_codes(codes)

        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))

    # ---------------- assign ----------------

    def assign_code(self, code: str, reg_number: int, grade_id: int):
        try:
            existing = self.code_repo.get_by_code(code)
            if existing is None:
                self.view.show_error("Code not found.")
                return
            if existing.reg_number is not None:
                self.view.show_error("Code already assigned to a candidate.")
                return

            self.code_repo.assign_to_candidate(code, reg_number, grade_id)
            self.session.commit()
            self.view.show_success(
                f"Code {code} assigned to candidate {reg_number}."
            )
        except Exception as e:
            self.session.rollback()
            self.view.show_error(str(e))