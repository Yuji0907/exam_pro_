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

from controllers.code_controller import CodeController
from controllers.willaya_controller import WillayaController
from controllers.subject_controller import SubjectController

from models.willaya_model import WillayaModel
from models.subject_model import SubjectModel
from models.code_model import CodeModel


class CodeGenerator(QWidget):

    def __init__(self, session: Session):
        super().__init__()

        self.wilaya_data = None
        self.subject_data = None

        self.wilaya_combo = QComboBox()
        self.subject_combo = QComboBox()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(10000)
        self.quantity_spin.setValue(10)
        self.setWindowTitle("code generator")

        self.table = QTableWidget()

        # Controllers
        self.code_controller = CodeController(
            view=self,
            session=session
        )

        self.willaya_controller = WillayaController(
            view=self,
            session=session
        )

        self.subject_controller = SubjectController(
            view=self,
            session=session
        )

        # Load data
        self.willaya_controller.load_willayas()
        self.subject_controller.load_subjects()

        # Signals
        self.wilaya_combo.currentIndexChanged.connect(
            self.onWillayaChanged
        )

        self.subject_combo.currentIndexChanged.connect(
            self.onSubjectChanged
        )

        # Table
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Code"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        # Button
        self.generate_button = QPushButton("Generate Codes")
        self.generate_button.clicked.connect(
            self.generate_code
        )

        self.print_button = QPushButton("Print")
        # Quantity layout
        quantity_layout = QHBoxLayout()

        quantity_layout.addWidget(
            QLabel("Quantity")
        )

        quantity_layout.addWidget(
            self.quantity_spin
        )

        # Combo layout
        combo_layout = QHBoxLayout()

        combo_layout.addWidget(
            QLabel("Wilaya")
        )

        combo_layout.addWidget(
            self.wilaya_combo
        )

        combo_layout.addWidget(
            QLabel("Subject")
        )

        combo_layout.addWidget(
            self.subject_combo
        )

        # Main layout
        layout = QVBoxLayout()

        layout.addLayout(combo_layout)
        layout.addLayout(quantity_layout)

        layout.addWidget(self.table)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.print_button)

        self.setLayout(layout)

        self.setFixedSize(500, 500)

    # --------------------------------------------------
    # Data loading
    # --------------------------------------------------

    def load_willayas(
        self,
        willayas: list[WillayaModel]
    ):
        self.wilaya_combo.clear()

        for willaya in willayas:
            self.wilaya_combo.addItem(
                willaya.willaya,
                willaya.id
            )

        if self.wilaya_combo.count() > 0:
            self.wilaya_data = self.wilaya_combo.itemData(0)

    def load_subjects(
        self,
        subjects: list[SubjectModel]
    ):
        self.subject_combo.clear()

        for subject in subjects:
            self.subject_combo.addItem(
                subject.subject,
                subject.id
            )

        if self.subject_combo.count() > 0:
            self.subject_data = self.subject_combo.itemData(0)

    # --------------------------------------------------
    # Selection
    # --------------------------------------------------

    def onWillayaChanged(self, index):
        self.table.setRowCount(0)
        self.wilaya_data = self.wilaya_combo.itemData(index)

    def onSubjectChanged(self, index):
        self.table.setRowCount(0)

        self.subject_data = self.subject_combo.itemData(index)

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate_code(self):

        if self.wilaya_data is None:
            self.show_error("Please select a Wilaya.")
            return

        if self.subject_data is None:
            self.show_error("Please select a Subject.")
            return

        quantity = self.quantity_spin.value()

        self.code_controller.generate_codes(
            willaya_id=self.wilaya_data,
            subject_id=self.subject_data,
            quantity=quantity
        )

    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    def display_codes(self, codes: list[CodeModel]):

        self.table.setRowCount(0)

        for code in codes:

            row = self.table.rowCount()

            self.table.insertRow(row)

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(code.code))
            )

    # --------------------------------------------------
    # Error
    # --------------------------------------------------

    def show_error(self, error):

        print(error)