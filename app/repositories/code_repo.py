from sqlalchemy.orm import Session
from sqlalchemy import select, and_

from database.orm_models import Code as CodeORM
from database.orm_models import CodeFormat as CodeFormatORM
from models.code_model import CodeModel


class CodeRepository:

    def __init__(self, session: Session):
        self.session = session

    # --------------------------------------------------
    # ORM -> Domain
    # --------------------------------------------------

    def _to_model(
        self,
        code: CodeORM
    ) -> CodeModel:

        return CodeModel(
            id=code.id,
            file_number=code.file_number,
            code=code.code,
            format_willaya_id=code.format_willaya_id,
            format_subject_id=code.format_subject_id,
            packet_number=code.packet_number
        )

    # --------------------------------------------------
    # Get all
    # --------------------------------------------------

    def get_all(self) -> list[CodeModel]:

        codes = (
            self.session
            .query(CodeORM)
            .all()
        )

        return [
            self._to_model(code)
            for code in codes
        ]

    # --------------------------------------------------
    # Get by ID
    # --------------------------------------------------

    def get_by_id(
        self,
        code_id: int
    ) -> CodeModel | None:

        code = self.session.get(
            CodeORM,
            code_id
        )

        if code is None:
            return None

        return self._to_model(code)
    
    def get_by_id_orm(
        self,
        code_id: int
    ) -> CodeORM :

        code = self.session.get(
            CodeORM,
            code_id
        )

        if code is None:
            return None

        return code

    # --------------------------------------------------
    # Get by code string
    # --------------------------------------------------

    def get_by_code(
        self,
        code: str
    ) -> CodeModel | None:

        result = (
            self.session
            .query(CodeORM)
            .filter(
                CodeORM.code == code
            )
            .first()
        )

        if result is None:
            return None

        return self._to_model(result)

    # --------------------------------------------------
    # Get candidate codes
    # --------------------------------------------------

    def get_by_file_number(
        self,
        file_number: int
    ) -> list[CodeModel]:

        codes = (
            self.session
            .query(CodeORM)
            .filter(
                CodeORM.file_number == file_number
            )
            .all()
        )

        return [
            self._to_model(code)
            for code in codes
        ]

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create(
        self,
        code: str,
        format_willaya_id: int,
        format_subject_id: int,
        file_number: int | None = None
    ) -> tuple[CodeModel, bool]:

        existing = self.get_by_code(code)

        if existing:
            return existing, True

        code_orm = CodeORM(
            code=code,
            file_number=file_number,
            format_willaya_id=format_willaya_id,
            format_subject_id=format_subject_id
        )

        self.session.add(code_orm)
        self.session.commit()
        self.session.refresh(code_orm)

        return self._to_model(code_orm), False

    # --------------------------------------------------
    # Get by code format 
    # --------------------------------------------------
    def get_by_codeformat(
        self,
        code_format: str
    ) -> list[CodeModel]:
        stmt = (
            select(CodeORM)
            .join(
                CodeFormatORM,
                and_(
                    CodeFormatORM.willaya_id == CodeORM.format_willaya_id,
                    CodeFormatORM.subject_id == CodeORM.format_subject_id
                )
            )
            .where(
                (
                    CodeFormatORM.willaya_format
                    + CodeFormatORM.subject_format
                    + CodeFormatORM.value_format
                ) == code_format
            )
        )

        result = self.session.execute(stmt).scalars().all()
        return result
    # --------------------------------------------------
    # Create multiple codes
    # --------------------------------------------------

    def create_many(
        self,
        codes: list[str],
        format_willaya_id: int,
        format_subject_id: int
    ) -> list[CodeModel]:

        code_objects = [
            CodeORM(
                code=code,
                file_number=None,
                format_willaya_id=format_willaya_id,
                format_subject_id=format_subject_id
            )
            for code in codes
        ]

        self.session.add_all(code_objects)

        self.session.commit()

        for code in code_objects:
            self.session.refresh(code)

        return [
            self._to_model(code)
            for code in code_objects
        ]

    # --------------------------------------------------
    # Assign code to candidate
    # --------------------------------------------------

    def assign_to_candidate(
        self,
        code: str,
        file_number: int
    ) -> CodeModel | None:

        code_orm = (
            self.session
            .query(CodeORM)
            .filter(
                CodeORM.code == code
            )
            .first()
        )

        if code_orm is None:
            return None

        code_orm.file_number = file_number

        self.session.commit()
        self.session.refresh(code_orm)

        return self._to_model(code_orm)

    
    # --------------------------------------------------
    # update
    # --------------------------------------------------

    def update(
        self,code : CodeModel ) -> CodeModel:
        orm_code = self.get_by_id_orm(code_id=code.id)
        print("===================")
        if not orm_code:
            raise ValueError(
                f"No code found for id={code.id}, "
            )

        orm_code.code = code.code
        orm_code.file_number = code.file_number
        orm_code.format_subject_id = code.format_subject_id
        orm_code.format_willaya_id = code.format_willaya_id
        orm_code.packet_number = code._packet_number
        
        self.session.commit()
        self.session.refresh(orm_code)
        return self._to_model(orm_code)
    
    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(
        self,
        code: str
    ) -> bool:

        code_orm = (
            self.session
            .query(CodeORM)
            .filter(
                CodeORM.code == code
            )
            .first()
        )

        if code_orm is None:
            return False

        self.session.delete(code_orm)
        self.session.commit()

        return True