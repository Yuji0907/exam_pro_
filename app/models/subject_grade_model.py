from PyQt5.QtCore import QObject, pyqtSignal
from models.grade_model import GradeModel
from models.subject_model import SubjectModel

class Subject_grade(QObject):
    subjects_changed = pyqtSignal(list)
    grade_changed = pyqtSignal(object)
    current_subject_changed = pyqtSignal(int)

    def __init__(self,
                 id=None,
                 grade: GradeModel = None,
                 subjects:list[SubjectModel]=None,
                 current_subject: int = 0):
        super().__init__()
        self._id = id
        self._grade = grade
        self._subjects = subjects if subjects is not None else []
        self._current_subject = current_subject

    # ---------- id ----------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # ---------- grade ----------
    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if value != self._grade:
            self._grade = value
            self.grade_changed.emit(value)

    # ---------- subjects ----------
    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        if value != self._subjects:
            self._subjects = value
            self.subjects_changed.emit(value)

    # ---------- current_subject ----------
    @property
    def current_subject(self):
        return self._current_subject

    @current_subject.setter
    def current_subject(self, value):
        if value != self._current_subject:
            self._current_subject = value
            self.current_subject_changed.emit(value)