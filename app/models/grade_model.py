from PyQt5.QtCore import QObject, pyqtSignal
 
 
class GradeModel(QObject):
 
    name_changed = pyqtSignal(str)
 
    def __init__(self, id=None, name=""):
        super().__init__()
        self._id = id
        self._name = name
 
    @property
    def name(self):
        return self._name
    @property
    def id(self):
        return self._id
 
    @name.setter
    def name(self, value):
        if value != self._name:
            self._name = value
            self.name_changed.emit(value)
 