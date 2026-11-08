from PyQt5.QtWidgets import (
    QWidget, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QHeaderView,
)
from sqlalchemy.orm import Session

from controllers.code_controller import CodeController
from models.code_model import CodeModel


class CodeGenerator(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.grade_id = None
        self.center_id = None
        self.subject_id = None

        self.grade_combo = QComboBox()
        self.center_combo = QComboBox()
        self.subject_combo = QComboBox()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(10000)
        self.quantity_spin.setValue(10)
        self.setWindowTitle("code generator")

        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Code"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.message = QLabel("")
        self.message.setObjectName("W_error")

        self.generate_button = QPushButton("Generate Codes")
        self.generate_button.clicked.connect(self.generate_code)
        self.print_button = QPushButton("Print")

        # Layouts
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Grade"))
        combo_layout.addWidget(self.grade_combo)
        combo_layout.addWidget(QLabel("Center"))
        combo_layout.addWidget(self.center_combo)
        combo_layout.addWidget(QLabel("Subject"))
        combo_layout.addWidget(self.subject_combo)

        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("Quantity"))
        quantity_layout.addWidget(self.quantity_spin)

        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        layout.addLayout(quantity_layout)
        layout.addWidget(self.message)
        layout.addWidget(self.table)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.print_button)
        self.setLayout(layout)
        self.setFixedSize(650, 500)

        # Controller + initial load (signals connected afterwards)
        self.code_controller = CodeController(view=self, session=session)
        self.code_controller.load_grades()
        self.on_grade_changed(self.grade_combo.currentIndex())

        self.grade_combo.currentIndexChanged.connect(self.on_grade_changed)
        self.center_combo.currentIndexChanged.connect(self.on_selection_changed)
        self.subject_combo.currentIndexChanged.connect(self.on_selection_changed)

    # ---------------- combos ----------------

    def _fill(self, combo: QComboBox, items):
        combo.blockSignals(True)
        combo.clear()
        for item_id, label in items:
            combo.addItem(label, item_id)
        combo.blockSignals(False)

    def load_grades(self, grades):
        self._fill(self.grade_combo, grades)

    def load_centers(self, centers):
        self._fill(self.center_combo, centers)

    def load_subjects(self, subjects):
        self._fill(self.subject_combo, subjects)

    def on_grade_changed(self, index):
        self.grade_id = self.grade_combo.itemData(index)
        if self.grade_id is None:
            return
        self.code_controller.load_centers(self.grade_id)
        self.code_controller.load_subjects(self.grade_id)
        self.on_selection_changed()

    def on_selection_changed(self, _index=None):
        self.table.setRowCount(0)
        self.clear_message()
        self.center_id = self.center_combo.currentData()
        self.subject_id = self.subject_combo.currentData()

    # ---------------- generate ----------------

    def generate_code(self):
        if self.grade_id is None:
            self.show_error("Please select a Grade.")
            return
        if self.center_id is None:
            self.show_error("Please select a Center.")
            return
        if self.subject_id is None:
            self.show_error("Please select a Subject.")
            return

        self.code_controller.generate_codes(
            center_id=self.center_id,
            grade_id=self.grade_id,
            subject_id=self.subject_id,
            quantity=self.quantity_spin.value(),
        )

    # ---------------- display ----------------

    def display_codes(self, codes: list[CodeModel]):
        self.table.setRowCount(0)
        for code in codes:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(code.code)))

    # ---------------- messages ----------------

    def clear_message(self):
        self.message.setText("")

    def show_error(self, error):
        self.message.setText(str(error))

    def show_success(self, text):
        self.message.setText(str(text))