from PyQt5.QtCore import QObject, pyqtSignal


class CodeFormat(QObject):
    center_format_changed = pyqtSignal(str)
    grade_format_changed = pyqtSignal(str)
    subject_format_changed = pyqtSignal(str)
    value_format_changed = pyqtSignal(str)

    def __init__(
        self,
        center_id=None,
        grade_id=None,
        subject_id=None,
        center_format="",
        grade_format="",
        subject_format="",
        value_format="",
    ):
        super().__init__()
        self.center_id = center_id
        self.grade_id = grade_id
        self.subject_id = subject_id
        self._center_format = center_format or ""
        self._grade_format = grade_format or ""
        self._subject_format = subject_format or ""
        self._value_format = value_format or ""

    @property
    def center_format(self):
        return self._center_format

    @center_format.setter
    def center_format(self, value):
        if value != self._center_format:
            self._center_format = value
            self.center_format_changed.emit(value)

    @property
    def grade_format(self):
        return self._grade_format

    @grade_format.setter
    def grade_format(self, value):
        if value != self._grade_format:
            self._grade_format = value
            self.grade_format_changed.emit(value)

    @property
    def subject_format(self):
        return self._subject_format

    @subject_format.setter
    def subject_format(self, value):
        if value != self._subject_format:
            self._subject_format = value
            self.subject_format_changed.emit(value)

    @property
    def value_format(self):
        return self._value_format

    @value_format.setter
    def value_format(self, value):
        if value != self._value_format:
            self._value_format = value
            self.value_format_changed.emit(value)