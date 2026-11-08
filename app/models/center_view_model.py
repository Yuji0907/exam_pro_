
from PyQt5.QtCore import QObject, pyqtSignal
from models.willaya_model import WillayaModel

class Center_model(QObject):
    willayas_changed = pyqtSignal(list)
    center_changed = pyqtSignal(str)
    
    def __init__(self, id=None, willayas=[],center=""):
        super().__init__()
        self._id = id
        self._willayas:list[WillayaModel] = willayas
        self._center = center

    @property
    def willayas(self):
        return self._willayas
    
    @property
    def  center(self):
        return self._center
    
    @property
    def id(self):
        return self._id

    @willayas.setter
    def willayas(self, value):
        if value != self.willayas:
            self._willayas = value
            self.willayas_changed.emit(value)



