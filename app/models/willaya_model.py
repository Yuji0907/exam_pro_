
from PyQt5.QtCore import QObject, pyqtSignal


class WillayaModel(QObject):
    willaya_changed = pyqtSignal(str)

    def __init__(self, id=None, willaya=""):
        super().__init__()
        self._id = id
        self._willaya = willaya

    @property
    def willaya(self):
        return self._willaya
    @property
    def id(self):
        return self._id

    @willaya.setter
    def willaya(self, value):
        if value != self.willaya:
            self._willaya = value
            self.willaya_changed.emit(value)



