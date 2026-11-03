
from PyQt5.QtCore import QObject, pyqtSignal


class CodeModel(QObject):
    code_changed = pyqtSignal(str)
    format_willaya_id_changed = pyqtSignal(int)
    format_subject_id_changed = pyqtSignal(int)
    packet_number_changed = pyqtSignal(int)

    def __init__(self, id=None,file_number=0, code="", 
                 format_willaya_id=None, 
                 format_subject_id=None,
                 packet_number=None):
        super().__init__()
        self.id = id
        self._code = code
        self._format_willaya_id = format_willaya_id 
        self._format_subject_id = format_subject_id
        self._file_number = file_number
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
    def packet_number(self):
        return self._packet_number

    @packet_number.setter
    def packet_number(self, value):
        if value != self._packet_number:
            self._packet_number = value
            self.packet_number_changed.emit(value)

    @property
    def file_number(self):
        return self._file_number

    @file_number.setter
    def file_number(self, value):
        if value != self._file_number:
            self._file_number = value

    @property
    def format_willaya_id(self):
        return self._format_willaya_id

    @format_willaya_id.setter
    def format_willaya_id(self, value):
        if value != self._format_willaya_id:
            self._format_willaya_id = value
            self.format_willaya_id_changed.emit(value)
    @property
    def format_subject_id(self):
        return self._format_subject_id

    @format_subject_id.setter
    def format_subject_id(self, value):
        if value != self._format_subject_id:
            self._format_subject_id = value
            self.format_subject_id_changed.emit(value)

        