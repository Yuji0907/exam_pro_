

from PyQt5.QtCore import QObject, pyqtSignal


class Packet(QObject):


    name_changed = pyqtSignal(str)
    total_number_changed = pyqtSignal(int)
    current_count_changed = pyqtSignal(int)
    def __init__(self, willaya_id=None,subject_id=None
                 , number=None,total_number=0,name=None,current_count=0):
        super().__init__()
        self.willaya_id =willaya_id 
        self.subject_id =subject_id 
        self.number =number 
        self._total_number =total_number 
        self._name = name
        self._current_count =current_count 


    @property
    def total_number(self):
        return self._total_number

    @total_number.setter
    def total_number(self, value):
        if value != self._total_number:
            self._total_number = value
            self.total_number_changed.emit(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value != self._name:
            self._name = value
            self.name_changed.emit(value)

    @property
    def current_count(self):
        return self._current_count

    @current_count.setter
    def current_count(self, value):
        if value != self._current_count:
            self._current_count = value
            self.current_count_changed.emit(value)


