from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QLabel, QHeaderView, QAbstractItemView,
)
from sqlalchemy.orm import Session

from controllers.code_format_controller import CodeFormatController
from models.code_format_model import CodeFormat as CodeFormatModel

COL_CENTER, COL_GRADE, COL_SUBJECT, COL_VALUE = range(4)


class CodeFormat(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.grade_id = None
        self.center_id = None
        self.subject_id = None

        self.grade_combo = QComboBox()
        self.center_combo = QComboBox()
        self.subject_combo = QComboBox()
        self.table = QTableWidget(1, 4)
        self.setWindowTitle("code format")

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r") as file:
            self.setStyleSheet(file.read())
        self.setObjectName("Container")
        self.setFixedSize(650, 600)

        self.controller = CodeFormatController(view=self, session=session)
        self.controller.assign_default()

        # Message
        self.message = QLabel("")
        self.message.setObjectName("W_error")
        message_row = QHBoxLayout()
        message_row.addStretch()
        message_row.addWidget(self.message)
        message_row.addStretch()

        # Table
        self.table.setHorizontalHeaderLabels(["center", "grade", "subject", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellChanged.connect(self.on_cell_changed)

        # Button
        self.save_button = QPushButton("assign format")
        self.save_button.setObjectName("Button")
        self.save_button.clicked.connect(self.save_format)

        # Layout
        combo_layout = QHBoxLayout()
        combo_layout.addWidget(QLabel("Grade"))
        combo_layout.addWidget(self.grade_combo)
        combo_layout.addWidget(QLabel("Center"))
        combo_layout.addWidget(self.center_combo)
        combo_layout.addWidget(QLabel("Subject"))
        combo_layout.addWidget(self.subject_combo)

        layout = QVBoxLayout()
        layout.addLayout(combo_layout)
        layout.addLayout(message_row)
        layout.addWidget(self.table)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Connect combos after the first load to avoid half-filled reloads
        self.controller.load_grades()
        self.on_grade_changed(self.grade_combo.currentIndex())
        self.grade_combo.currentIndexChanged.connect(self.on_grade_changed)
        self.center_combo.currentIndexChanged.connect(self.reload_format)
        self.subject_combo.currentIndexChanged.connect(self.reload_format)

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
        self.controller.load_centers(self.grade_id)
        self.controller.load_subjects(self.grade_id)
        self.reload_format()

    def reload_format(self, _index=None):
        self.clear_message()
        self.cleartable()
        self.center_id = self.center_combo.currentData()
        self.subject_id = self.subject_combo.currentData()
        if None in (self.grade_id, self.center_id, self.subject_id):
            return
        self.controller.load_code_format(self.center_id, self.grade_id, self.subject_id)

    # ---------------- table ----------------

    def cleartable(self):
        self.table.blockSignals(True)
        self.table.setRowCount(1)
        self.table.clearContents()
        self.table.blockSignals(False)

    def _cell(self, column: int) -> str:
        item = self.table.item(0, column)
        return item.text().strip() if item is not None else ""

    def on_cell_changed(self, row, column):
        if row != 0 or column not in (COL_CENTER, COL_GRADE):
            return
        text = self._cell(column)
        if column == COL_CENTER:
            ok = self.controller.check_center_format(text, self.center_id)
            error = "le code center existe deja ..."
        else:
            ok = self.controller.check_grade_format(text, self.grade_id)
            error = "le code grade existe deja ..."
        if not ok:
            self.message.setText(error)
            self.table.blockSignals(True)
            self.table.item(0, column).setText("")
            self.table.blockSignals(False)
        else:
            self.clear_message()

    def display_code_format(self, code_format: CodeFormatModel):
        self.table.blockSignals(True)
        self.table.setRowCount(1)
        self.table.clearContents()
        self.table.setItem(0, COL_CENTER, QTableWidgetItem(code_format.center_format))
        self.table.setItem(0, COL_GRADE, QTableWidgetItem(code_format.grade_format))
        self.table.setItem(0, COL_SUBJECT, QTableWidgetItem(code_format.subject_format))
        self.table.setItem(0, COL_VALUE, QTableWidgetItem(code_format.value_format))
        self.table.blockSignals(False)
        self.check_editable()

    def check_editable(self):
        if None in (self.center_id, self.grade_id, self.subject_id):
            return
        editable = self.controller.check_editable(
            self.center_id, self.grade_id, self.subject_id
        )
        self.table.setEditTriggers(
            QAbstractItemView.AllEditTriggers if editable
            else QAbstractItemView.NoEditTriggers
        )
        self.save_button.setEnabled(editable)

    # ---------------- actions ----------------

    def save_format(self):
        center_format = self._cell(COL_CENTER)
        grade_format = self._cell(COL_GRADE)
        if not center_format or not grade_format:
            self.show_error("code format cellules vide !")
            return
        self.controller.save_code_format(
            self.center_id, self.grade_id, self.subject_id,
            center_format, grade_format,
            self._cell(COL_SUBJECT), self._cell(COL_VALUE),
        )

    # ---------------- messages ----------------

    def clear_message(self):
        self.message.setText("")

    def show_error(self, error):
        self.message.setText(str(error))

    def show_success(self, text):
        self.message.setText(str(text))