from pathlib import Path

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QWidget,
)
from sqlalchemy.orm import Session

from controllers.candidate_controller import CandidateController
from models.candidate_model import CandidateModel
from repositories.willaya_repo import WillayaRepository


class CandidateView(QWidget):
    def __init__(self, session: Session):
        super().__init__()
        self.setWindowTitle("Candidates")
        self.setMinimumSize(760, 560)

        style_path = Path(__file__).parent.parent / "styles" / "components.qss"
        with open(style_path, "r", encoding="utf-8") as style_file:
            self.setStyleSheet(style_file.read())

        self._candidates: dict[int, CandidateModel] = {}
        self._willaya_names: dict[int, str] = {}
        self._editing_file_number: int | None = None

        self.controller = CandidateController(view=self, session=session)
        self.willaya_repository = WillayaRepository(session)

        self._build_ui()
        self._load_willayas()
        self.controller.load_candidates()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Candidates")
        title.setObjectName("SideBarTitle")
        layout.addWidget(title)


        search_row = QHBoxLayout()
        search_row.addWidget(QLabel("Search"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by file number or name")
        self.search_input.textChanged.connect(self.filter_candidates)
        search_row.addWidget(self.search_input)
        layout.addLayout(search_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["File number", "First name", "Last name", "Wilaya"]
        )
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

    def _load_willayas(self) -> None:
        for willaya in self.willaya_repository.get_all():
# ?            self.willaya_combo.addItem(willaya.willaya, willaya.id)
            self._willaya_names[willaya.id] = willaya.willaya

    def display_candidates(self, candidates: list[CandidateModel]) -> None:
        self._candidates = {
            candidate.file_number: candidate for candidate in candidates
        }
        self.table.setRowCount(len(candidates))

        for row, candidate in enumerate(candidates):
            values = (
                str(candidate.file_number),
                candidate.first_name,
                candidate.last_name,
                self._willaya_names.get(candidate.willaya_id, "Not set"),
            )
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

        self.filter_candidates(self.search_input.text())

    def display_candidate(self, candidate: CandidateModel) -> None:
        self._select_candidate(candidate.file_number)
    def filter_candidates(self, query: str) -> None:
        query = query.strip().casefold()
        for row in range(self.table.rowCount()):
            matches = not query or any(
                query in (self.table.item(row, column).text().casefold())
                for column in range(self.table.columnCount())
                if self.table.item(row, column) is not None
            )
            self.table.setRowHidden(row, not matches)

