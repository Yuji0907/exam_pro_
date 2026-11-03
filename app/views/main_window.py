from PyQt5.QtWidgets import (
    QWidget,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QHeaderView
)

from sqlalchemy.orm import Session

from pathlib import Path
import qtawesome as qta

class MainWindow(QWidget):

    def __init__(self, session: Session):
        super().__init__()
        self.showMaximized()
        style_path = Path(__file__).parent.parent  / "styles" / "style.qss"

        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)

        self.button = QPushButton()
        self.button.setText("younes")

        icon = qta.icon(
                'fa6s.house',
            color='#2563eb'
        )
        self.button.setIcon(icon)
        self.mainLayout.addWidget(self.button)
        self.setLayout(self.mainLayout)

        




