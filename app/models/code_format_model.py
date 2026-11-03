

from PyQt5.QtCore import QObject, pyqtSignal


class CodeFormat(QObject):

    willaya_format_changed = pyqtSignal(str)
    subject_format_changed = pyqtSignal(str)
    value_format_changed = pyqtSignal(str)
    def __init__(self, willaya_id=None,subject_id=None
                 , willaya_format="", subject_format="",value_format=""):
        super().__init__()
        self.willaya_id =willaya_id 
        self.subject_id =subject_id 
        self._willaya_format =willaya_format 
        self._subject_format =subject_format 
        self._value_format =value_format 


    @property
    def willaya_format(self):
        return self._willaya_format

    @willaya_format.setter
    def willaya_format(self, value):
        if value != self._willaya_format:
            self._willaya_format = value
            self.willaya_format_changed.emit(value)


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

