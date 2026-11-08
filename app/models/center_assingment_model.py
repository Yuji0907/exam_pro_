
from PyQt5.QtCore import QObject, pyqtSignal
from models.center_view_model import Center_model


class Center_Assingn_model(QObject):
    centers_changed = pyqtSignal(list)
    grade_changed = pyqtSignal(str)
    current_center_changed = pyqtSignal(int)
    
    def __init__(self, id=None,grade="", centers=[],current_center=0):
        super().__init__()
        self._id = id
        self._centers:list[Center_model] = centers
        self._grade = grade
        self._current_center=current_center

    @property
    def centers(self):
        return self._centers
    
    @property
    def  grade(self):
        return self._grade
    
    @property
    def  current_center(self):
        return self._current_center
    
    @property
    def id(self):
        return self._id




    @centers.setter
    def centers(self, value):
        if value != self.centers:
            self._centers = value
            self.centers_changed.emit(value)

    @current_center.setter
    def current_center(self, value):
        if value != self.current_center:
            self._current_center = value
            self.current_center_changed.emit(value)

    @grade.setter
    def grade(self, value):
        if value != self.grade:
            self._grade = value
            self.grade_changed.emit(value)



