
from PyQt5.QtCore import QObject, pyqtSignal


class EvalModel(QObject):
    code_id_changed = pyqtSignal(int)
    eval_value_changed = pyqtSignal(float)

    def __init__(self, id=None,code_id=0, eval_value=0):
        super().__init__()
        self.id = id
        self._code_id = code_id
        self._eval_value = eval_value


    @property
    def code_id(self):
        return self._code_id

    @code_id.setter
    def code(self, value):
        if value != self._code_id:
            self._code_id = value
            self.code_id_changed.emit(value)

    @property
    def grade(self):
        return self._eval_value


    @grade.setter
    def eval_value(self, value):
        if value != self._eval_value:
            self._eval_value = value
            self.eval_value_changed.emit(value)

        