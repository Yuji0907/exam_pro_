

from datetime import date
from sqlalchemy import (
    Float,
    Integer,
    String,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
    Date
)
from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped,
    relationship,
)

Base = declarative_base()

class Grade(Base):                      
    __tablename__ = "grade"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    candidates: Mapped[list["Candidate"]] = relationship(back_populates="grade")
    code_formats: Mapped[list["CodeFormat"]] = relationship(back_populates="grade")
    assignments: Mapped[list["CenterAssignment"]] = relationship(back_populates="grade")
    grade_to_subjects: Mapped[list["Subject_to_grade"]] = relationship(back_populates="grade")
    


class Willaya(Base):
    __tablename__ = "willaya"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    willaya: Mapped[str] = mapped_column(String(100), nullable=False)
    candidates: Mapped[list["Candidate"]] = relationship(back_populates="willaya")




  
    
class Center(Base):
    __tablename__ = "center"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    assignments: Mapped[list["CenterAssignment"]] = relationship(back_populates="center")
    code_formats: Mapped[list["CodeFormat"]] = relationship(back_populates="center")
    packets: Mapped[list["Packet"]] = relationship(back_populates="center")



class CenterAssignment(Base):
    __tablename__ = "center_assignment"

    grade_id: Mapped[int] = mapped_column(ForeignKey("grade.id"), primary_key=True)
    willaya_id: Mapped[int] = mapped_column(ForeignKey("willaya.id"), primary_key=True)
    center_id: Mapped[int] = mapped_column(ForeignKey("center.id"), nullable=False)

    grade: Mapped["Grade"] = relationship(back_populates="assignments")
    willaya: Mapped["Willaya"] = relationship()
    center: Mapped["Center"] = relationship(back_populates="assignments")



class Subject_to_grade(Base):
    __tablename__ = "subject_to_grade"

    Subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"), primary_key=True)
    grade_id: Mapped[int] = mapped_column(ForeignKey("grade.id"), primary_key=True)
    coeff: Mapped[int] = mapped_column(Integer,nullable=False)


    grade: Mapped["Grade"] = relationship(back_populates="grade_to_subjects")
    subject: Mapped["Subject"] = relationship(back_populates="subject_to_grades")


class Subject(Base):
    __tablename__ = "subject"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    subject: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )



    code_formats: Mapped[list["CodeFormat"]] = relationship(
        back_populates="subject"
    )

    packets: Mapped[list["Packet"]] = relationship(
        back_populates="subject"
    )

    subject_to_grades:Mapped[list["Subject_to_grade"]] = relationship(
        back_populates="subject"
    )



class CodeFormat(Base):
    __tablename__ = "codeformat"

    center_id: Mapped[int] = mapped_column(Integer,ForeignKey("center.id"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(Integer,ForeignKey("subject.id"), primary_key=True)
    grade_id: Mapped[int] = mapped_column(Integer,ForeignKey("grade.id"), primary_key=True)

    center_format: Mapped[str] = mapped_column(String(20), nullable=False)  
    grade_format: Mapped[str] = mapped_column(String(20), nullable=False)  
    subject_format: Mapped[str | None] = mapped_column(String(20), nullable=True)
    value_format: Mapped[str | None] = mapped_column(String(50), nullable=True)

    grade: Mapped["Grade"] = relationship(back_populates="code_formats")
    center: Mapped["Center"] = relationship(back_populates="code_formats")
    subject: Mapped["Subject"] = relationship(back_populates="code_formats")
    codes: Mapped[list["Code"]] = relationship(back_populates="code_format")




class Candidate(Base):
    __tablename__ = "candidate"

    reg_number: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    grade_id: Mapped[int] = mapped_column(ForeignKey("grade.id"), primary_key=True) 

    id:Mapped[int] =  mapped_column(Integer, unique=True,nullable=False)

    willaya_id: Mapped[int | None] = mapped_column(ForeignKey("willaya.id"), nullable=True)


    average: Mapped[float | None] = mapped_column(Float)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    birthday: Mapped[date | None] = mapped_column(Date,nullable=True)

    grade: Mapped["Grade"] = relationship(back_populates="candidates")
    willaya: Mapped["Willaya | None"] = relationship(back_populates="candidates")
    codes: Mapped[list["Code"]] = relationship(back_populates="candidate")

    # Derived center (grade + willaya -> center), read-only
    center: Mapped["Center | None"] = relationship(
        secondary="center_assignment",
        primaryjoin="and_(Candidate.grade_id == CenterAssignment.grade_id, "
                    "Candidate.willaya_id == CenterAssignment.willaya_id)",
        secondaryjoin="CenterAssignment.center_id == Center.id",
        viewonly=True,
        uselist=False,
    )

class Packet(Base):
    __tablename__ = "packet"

    center_id: Mapped[int] = mapped_column(ForeignKey("center.id"), primary_key=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"), primary_key=True)
    number: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String)
    total_number: Mapped[int] = mapped_column(Integer)
    current_count: Mapped[int] = mapped_column(Integer)

    center: Mapped["Center"] = relationship(back_populates="packets")
    subject: Mapped["Subject"] = relationship(back_populates="packets")
    codes: Mapped[list["Code"]] = relationship(back_populates="packet")



class Code(Base):
    __tablename__ = "code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    format_grade_id: Mapped[int] = mapped_column(Integer, nullable=False)
    format_center_id: Mapped[int] = mapped_column(Integer,nullable=False)
    format_subject_id: Mapped[int] = mapped_column(Integer,nullable=False)

    reg_number: Mapped[int | None] = mapped_column(Integer,nullable=True)
    candidate_grade_id: Mapped[int | None] = mapped_column(Integer,nullable=True)
    
    code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    packet_number: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["reg_number", "candidate_grade_id"],
            ["candidate.reg_number", "candidate.grade_id"],
        ),
        ForeignKeyConstraint(
            ["format_center_id", "format_subject_id","format_grade_id"],
            ["codeformat.center_id", "codeformat.subject_id","codeformat.grade_id"],
        ),
        ForeignKeyConstraint(
            ["format_center_id", "format_subject_id", "packet_number"],
            ["packet.center_id", "packet.subject_id", "packet.number"],
        ),
        UniqueConstraint(
            "format_grade_id",
            "format_center_id",
            "format_subject_id",
            name="uq_codeformat_center_grade_subject"
        )
    )

    candidate: Mapped["Candidate | None"] = relationship(back_populates="codes")
    code_format: Mapped["CodeFormat"] = relationship(
        back_populates="codes", overlaps="packet,codes"
    )
    packet: Mapped["Packet | None"] = relationship(
        back_populates="codes", overlaps="code_format,codes"
    )
    evaluation: Mapped["Eval | None"] = relationship(back_populates="code", uselist=False)


class Eval(Base):
    __tablename__ = "eval"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    code_id: Mapped[int] = mapped_column(
        ForeignKey("code.id"),
        nullable=False,
        unique=True
    )

    eval_value: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    code: Mapped["Code"] = relationship(
        back_populates="evaluation"
    )