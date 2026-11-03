from pathlib import Path

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from sqlalchemy.orm import Session

from controllers.subject_controller import SubjectController
from models.subject_model import SubjectModel

# TODO
# change the id to be automatic

class SubjectsView(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.setWindowTitle("Subjects")
        self.setMinimumSize(640, 480)

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self._subjects: dict[int, SubjectModel] = {}
        self._editing_subject_id: int | None = None
        self.controller = SubjectController(view=self, session=session)

        self._build_ui()
        self.controller.load_subjects()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Subjects")
        title.setObjectName("SideBarTitle")
        layout.addWidget(title)

        form = QFormLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Required")
        self.id_input.setValidator(QIntValidator(1, 2147483647, self))
        self.name_input = QLineEdit()
        self.coefficient_input = QLineEdit()
        self.coefficient_input.setPlaceholderText("Required")
        self.coefficient_input.setValidator(QIntValidator(0, 2147483647, self))
        form.addRow("ID", self.id_input)
        form.addRow("Subject name", self.name_input)
        form.addRow("Coefficient", self.coefficient_input)
        layout.addLayout(form)

        actions = QHBoxLayout()
        self.save_button = QPushButton("Add subject")
        self.save_button.setObjectName("Button")
        self.save_button.clicked.connect(self.save_subject)
        self.edit_button = QPushButton("Edit selected")
        self.edit_button.clicked.connect(self.edit_selected)
        self.edit_button.setEnabled(False)
        self.delete_button = QPushButton("Delete selected")
        self.delete_button.clicked.connect(self.delete_selected)
        self.delete_button.setEnabled(False)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        actions.addWidget(self.save_button)
        actions.addWidget(self.edit_button)
        actions.addWidget(self.delete_button)
        actions.addWidget(self.clear_button)
        layout.addLayout(actions)

        self.message = QLabel("")
        self.message.setWordWrap(True)
        layout.addWidget(self.message)

        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by ID or subject name")
        self.search_input.textChanged.connect(self.filter_subjects)
        search_row.addWidget(self.search_input)
        layout.addLayout(search_row)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Subject", "Coefficient"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.itemSelectionChanged.connect(self._selection_changed)
        layout.addWidget(self.table)

    def load_subjects(self, subjects: list[SubjectModel]) -> None:
        self._subjects = {subject.id: subject for subject in subjects}
        self.table.setRowCount(len(subjects))

        for row, subject in enumerate(subjects):
            values = (str(subject.id), subject.subject, str(subject.coeff))
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

        self.filter_subjects(self.search_input.text())

    def _selection_changed(self) -> None:
        has_selection = bool(self.table.selectedItems())
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)

    def _selected_subject_id(self) -> int | None:
        selected = self.table.selectedItems()
        if not selected:
            return None
        return int(self.table.item(selected[0].row(), 0).text())

    def edit_selected(self) -> None:
        subject_id = self._selected_subject_id()
        if subject_id is None:
            self.show_error("Select a subject to edit.")
            return

        subject = self._subjects[subject_id]
        self._editing_subject_id = subject.id
        self.id_input.setText(str(subject.id))
        self.id_input.setReadOnly(True)
        self.name_input.setText(subject.subject)
        self.coefficient_input.setText(str(subject.coeff))
        self.save_button.setText("Save changes")

    def save_subject(self) -> None:
        subject_id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        coefficient_text = self.coefficient_input.text().strip()
        if not subject_id_text or not name or not coefficient_text:
            self.show_error("Enter an ID, subject name, and coefficient.")
            return

        subject_id = int(subject_id_text)
        coefficient = int(coefficient_text)
        if self._editing_subject_id is None:
            self.controller.create_subject(subject_id, name, coefficient)
            return

        subject = SubjectModel(
            id=self._editing_subject_id,
            subject=name,
            coeff=coefficient,
        )
        self.controller.update_subject(subject, name, coefficient)

    def delete_selected(self) -> None:
        subject_id = self._selected_subject_id()
        if subject_id is None:
            self.show_error("Select a subject to delete.")
            return

        confirmation = QMessageBox.question(
            self,
            "Delete subject",
            f"Delete subject {subject_id}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            self.controller.delete_subject(subject_id)
            if self._editing_subject_id == subject_id:
                self.clear_form()

    def clear_form(self) -> None:
        self._editing_subject_id = None
        self.id_input.clear()
        self.id_input.setReadOnly(False)
        self.name_input.clear()
        self.coefficient_input.clear()
        self.save_button.setText("Add subject")
        self.message.clear()

    def filter_subjects(self, query: str) -> None:
        query = query.strip().casefold()
        for row in range(self.table.rowCount()):
            matches = not query or any(
                query in self.table.item(row, column).text().casefold()
                for column in range(self.table.columnCount())
                if self.table.item(row, column) is not None
            )
            self.table.setRowHidden(row, not matches)

    def show_error(self, message: str) -> None:
        self.message.setObjectName("W_error")
        self.message.setStyleSheet("color: #ff2424;")
        self.message.setText(message)

    def show_success(self, message: str) -> None:
        self.message.setObjectName("ChekMessage")
        self.message.setStyleSheet("color: green;")
        self.message.setText(message)