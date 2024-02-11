import sys, os.path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QStackedLayout,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QTableView,
)
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel


class DBApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SQL Interface")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stacked_layout = QStackedLayout()
        layout.addLayout(self.stacked_layout)

        self.login_screen()
        self.show()

    def login_screen(self) -> None:
        login_page = QWidget()
        layout = QVBoxLayout()
        h_title_layout = QHBoxLayout()
        h_form_layout = QHBoxLayout()
        form_layout = QVBoxLayout()

        # Top Down Center
        layout.addStretch()
        layout.addLayout(h_title_layout)
        layout.addLayout(h_form_layout)
        layout.addStretch()

        # Title Center
        h_title_layout.addStretch()
        h_title_layout.addWidget(QLabel("Login Page"))
        h_title_layout.addStretch()
        h_title_layout.setContentsMargins(0, 0, 0, 25)

        # Forms Center
        h_form_layout.addStretch()
        h_form_layout.addLayout(form_layout)
        h_form_layout.addStretch()

        db_name = QLineEdit()
        login_button = QPushButton("Login")
        login_button.setAutoDefault(True)
        login_button.setEnabled(False)

        form_layout.addWidget(QLabel("DB Name (SQLite):"))
        form_layout.addWidget(db_name)
        form_layout.addWidget(login_button)

        login_page.setLayout(layout)
        self.stacked_layout.addWidget(login_page)

        # Enable button once forms filled
        db_name.textChanged.connect(lambda: self.check_forms(db_name, login_button))

        login_button.clicked.connect(lambda: self.switch_pages(db_name.text()))

    def check_forms(self, db_name: QLineEdit, login_button: QPushButton) -> None:
        if len(db_name.text()) > 0:
            login_button.setEnabled(True)
        else:
            login_button.setEnabled(False)

    def switch_pages(self, db_name: str) -> None:
        if self.connect_db(db_name):
            self.db_display()
            self.stacked_layout.setCurrentIndex(1)

    def connect_db(self, db_name: str) -> bool:
        self.db = QSqlDatabase.addDatabase("QSQLITE")

        if os.path.exists(f"{db_name}.db"):
            self.db.setDatabaseName(f"{db_name}.db")
            if not self.db.open():
                QMessageBox.critical(
                    None,
                    "Database Error",
                    f"Database Error: {self.db.lastError().databaseText()}",
                )
                return False
            return True
        else:
            QMessageBox.warning(
                None, "Database Name Error", f"No Database with name {db_name}.db"
            )
            return False

    def db_display(self) -> None:
        db_page = QWidget()
        layout = QGridLayout()
        sql_query = QLineEdit()
        sql_query_button = QPushButton("Run Query")

        layout.addWidget(QLabel("Database View"), 0, 0)
        layout.addWidget(QLabel("Run SQL Queries:"), 1, 0)
        layout.addWidget(sql_query, 2, 0, 1, 3)
        layout.addWidget(sql_query_button, 3, 2, 1, 1)

        table = QTableView()

        # default query
        query_model = QSqlQueryModel()
        query_model.setQuery(
            """
            SELECT * FROM users;
            """,
            self.db,
        )

        sql_query_button.clicked.connect(lambda: self.run_query(sql_query, query_model))

        if query_model.lastError().isValid():
            QMessageBox.critical(
                None, "Query Error", f"Query Error: {query_model.lastError().text()}"
            )

        table.setModel(query_model)
        table.resizeColumnsToContents()
        layout.addWidget(table, 4, 0, 1, 3)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        db_page.setLayout(layout)
        self.stacked_layout.addWidget(db_page)

    def run_query(self, sql_query: QLineEdit, query_model: QSqlQueryModel) -> None:
        query_text = sql_query.text()
        query_model.setQuery(
            f"""
            {query_text}
            """,
            self.db,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DBApp()
    app.exec()
