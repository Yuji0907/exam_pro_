from PyQt5.QtWidgets import QComboBox

class YComboBox(QComboBox):
    def __init__(self, items=None):
        super().__init__()

        if items:
            self.addItems(items)