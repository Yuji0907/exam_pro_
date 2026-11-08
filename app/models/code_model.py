from PyQt5.QtCore import QObject, pyqtSignal


class CodeModel(QObject):
    code_changed = pyqtSignal(str)
    format_center_id_changed = pyqtSignal(int)
    format_grade_id_changed = pyqtSignal(int)
    format_subject_id_changed = pyqtSignal(int)
    packet_number_changed = pyqtSignal(object)  # object: the value can be None

    def __init__(
        self,
        id=None,
        code="",
        format_center_id=None,
        format_grade_id=None,
        format_subject_id=None,
        reg_number=None,
        candidate_grade_id=None,
        packet_number=None,
    ):
        super().__init__()
        self.id = id
        self._code = code
        self._format_center_id = format_center_id
        self._format_grade_id = format_grade_id
        self._format_subject_id = format_subject_id
        self._reg_number = reg_number
        self._candidate_grade_id = candidate_grade_id
        self._packet_number = packet_number

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        if value != self._code:
            self._code = value
            self.code_changed.emit(value)

    @property
    def format_center_id(self):
        return self._format_center_id

    @format_center_id.setter
    def format_center_id(self, value):
        if value != self._format_center_id:
            self._format_center_id = value
            self.format_center_id_changed.emit(value)

    @property
    def format_grade_id(self):
        return self._format_grade_id

    @format_grade_id.setter
    def format_grade_id(self, value):
        if value != self._format_grade_id:
            self._format_grade_id = value
            self.format_grade_id_changed.emit(value)

    @property
    def format_subject_id(self):
        return self._format_subject_id

    @format_subject_id.setter
    def format_subject_id(self, value):
        if value != self._format_subject_id:
            self._format_subject_id = value
            self.format_subject_id_changed.emit(value)

    @property
    def reg_number(self):
        return self._reg_number

    @reg_number.setter
    def reg_number(self, value):
        self._reg_number = value

    @property
    def candidate_grade_id(self):
        return self._candidate_grade_id

    @candidate_grade_id.setter
    def candidate_grade_id(self, value):
        self._candidate_grade_id = value

    @property
    def packet_number(self):
        return self._packet_number

    @packet_number.setter
    def packet_number(self, value):
        if value != self._packet_number:
            self._packet_number = value
            self.packet_number_changed.emit(value)