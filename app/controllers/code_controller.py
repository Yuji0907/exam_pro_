from sqlalchemy.orm import Session
from utils.Barcode_gen import generate_barcode
from repositories.code_repo import CodeRepository
from repositories.code_format_repo import CodeFormatRepository
from repositories.willaya_repo import WillayaRepository
from repositories.subject_repo import SubjectRepository
import os

class CodeController:

    def __init__(
        self,
        view,
        session: Session
    ):
        self.view = view

        self.code_repo = CodeRepository(session)

        self.code_format_repo = CodeFormatRepository(session)
        self.subject_repo = SubjectRepository(session)
        self.willaya_repo = WillayaRepository(session)

    # --------------------------------------------------
    # Load codes
    # --------------------------------------------------

    def load_codes(self):

        codes = self.code_repo.get_all()

        self.view.display_codes(
            codes
        )

    # --------------------------------------------------
    # Generate codes
    # --------------------------------------------------

    def generate_codes(
        self,
        willaya_id: int,
        subject_id: int,
        quantity: int
    ):

        if quantity <= 0:

            self.view.show_error(
                "Quantity must be greater than zero."
            )

            return

        # Get format
        code_format = (
            self.code_format_repo
            .get_by_ids(
                willaya_id,
                subject_id
            )
        )
        willaya = self.willaya_repo.get_by_id(willaya_id).willaya
        subject = self.subject_repo.get_by_id(subject_id).subject
        if code_format is None:

            self.view.show_error(
                "No code format exists for "
                "this Wilaya and Subject."
            )

            return

        # Starting value
        start_string = code_format.value_format
        print(start_string)
        try:
            start = int(start_string)
        except ValueError:
            self.view.show_error(
                f"Invalid starting value: "
                f"{start_string}"
            )
            return
        width = len(start_string)
        generated_codes = []
        temp_codes:str = f"temp\\{willaya}\\{subject}"
        os.makedirs(temp_codes, exist_ok=True)
        for i in range(quantity):
            value = str(start + i).zfill(width)
            code = (
                f"{code_format.willaya_format}"
                f"{code_format.subject_format}"
                f"{value}"
            )
           
            generate_barcode(code,f"{temp_codes}\\{value}")
            generated_codes.append(code)
        print(generated_codes)

        # Save generated codes
        try:
            codes = self.code_repo.create_many(
                codes=generated_codes,
                format_willaya_id=willaya_id,
                format_subject_id=subject_id
            )

            # Update next starting value
            next_value = start + quantity
            print(next_value)

            code_format.value_format = (
                str(next_value).zfill(width)
            )

            self.code_format_repo.update(
                code_format
            )

            self.view.display_codes(
                codes
            )

        except Exception as e:

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Assign code
    # --------------------------------------------------

    def assign_code(self,code: str,file_number: int ):
        try:
            result = (
                self.code_repo.assign_to_candidate(code,file_number)
            )

            if result is None:
                self.view.show_error(
                    "Code not found."
                )
                return
            
            self.view.show_success(f"Code {code} assigned "f"to candidate {file_number}." )
        except Exception as e:
            print(str(e) )





    
    # --------------------------------------------------
    # Load candidate codes
    # --------------------------------------------------

    def load_candidate_codes(
        self,
        file_number: int
    ):

        codes = (
            self.code_repo
            .get_by_file_number(
                file_number
            )
        )

        self.view.display_codes(
            codes
        )