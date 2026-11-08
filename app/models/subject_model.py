
from PyQt5.QtCore import QObject, pyqtSignal


class SubjectModel(QObject):
    subject_changed = pyqtSignal(str)
    coeff_changed = pyqtSignal(int)

    def __init__(self, id=None, subject="", coeff=0):
        super().__init__()
        self._id = id
        self._subject = subject
        self._coeff = coeff

    @property
    def id(self):
        return self._id
    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if value != self.subject:
            self._subject = value
            self.subject_changed.emit(value)

    @property
    def coeff(self):
        return self._coeff

    @coeff.setter
    def coeff(self, value):
        if value != self._coeff:
            self._coeff = value
            self.coeff_changed.emit(value)

