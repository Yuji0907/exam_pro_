from PyQt5.QtCore import QObject, pyqtSignal
 
 
class CenterModel(QObject):
 
    name_changed = pyqtSignal(str)
 
    def __init__(self, id=None, name=""):
        super().__init__()
        self.id = id
        self._name = name
 
    @property
    def name(self):
        return self._name
 
    @name.setter
    def name(self, value):
        if value != self._name:
            self._name = value
            self.name_changed.emit(value)
 
 
class CenterAssignmentModel(QObject):
 
    center_id_changed = pyqtSignal(int)
    center_name_changed = pyqtSignal(int)
 
    def __init__(self, grade_id=None, willaya_id=None, center_id=None,center_name=None):
        super().__init__()
        # (grade_id, willaya_id) is the composite key, so it never changes
        self.grade_id = grade_id
        self.willaya_id = willaya_id
        self._center_id = center_id
        self._center_name = center_name

 
    @property
    def center_id(self):
        return self._center_id
 
    @center_id.setter
    def center_id(self, value):
        if value != self._center_id:
            self._center_id = value
            self.center_id_changed.emit(value)


    @property
    def center_name(self):
        return self._center_name
 
    @center_name.setter
    def center_name(self, value):
        if value != self._center_name:
            self._center_name = value
            self.center_name_changed.emit(value)
 