import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QStackedLayout,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableView,
)
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel


class DBApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PostgreSQL Interface")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stacked_layout = QStackedLayout()
        layout.addLayout(self.stacked_layout)

        self.login_screen()
        self.show()

    def login_screen(self):
        login_page = QWidget()
        layout = QVBoxLayout()
        h_title_layout = QHBoxLayout()
        h_form_layout = QHBoxLayout()
        form_layout = QFormLayout()

        # Top Down Center
        layout.addStretch()
        layout.addLayout(h_title_layout)
        layout.addLayout(h_form_layout)
        layout.addStretch()

        # Title Center
        h_title_layout.addStretch()
        h_title_layout.addWidget(QLabel("Login Page"))
        h_title_layout.addStretch()
        h_title_layout.setContentsMargins(0, 0, 0, 50)

        # Forms Center
        h_form_layout.addStretch()
        h_form_layout.addLayout(form_layout)
        h_form_layout.addStretch()

        username_line = QLineEdit()
        password_line = QLineEdit()
        login_button = QPushButton("Login")
        login_button.setEnabled(False)

        form_layout.addRow("DB Username:", username_line)
        form_layout.addRow("DB Password:", password_line)
        form_layout.addWidget(login_button)

        login_page.setLayout(layout)
        self.stacked_layout.addWidget(login_page)

        # Enable button once forms filled
        username_line.textChanged.connect(
            lambda: self.check_forms(username_line, password_line, login_button)
        )
        password_line.textChanged.connect(
            lambda: self.check_forms(username_line, password_line, login_button)
        )

        login_button.clicked.connect(
            lambda: self.switch_pages(username_line.text(), password_line.text())
        )

    def check_forms(
        self,
        username_line: QLineEdit,
        password_line: QLineEdit,
        login_button: QPushButton,
    ) -> None:
        if len(username_line.text()) > 0 and len(password_line.text()) > 0:
            login_button.setEnabled(True)
        else:
            login_button.setEnabled(False)

    def switch_pages(self, db_username: str, db_password: str):
        db = QSqlDatabase()
        if self.connect_db(db, db_username, db_password):
            self.db_display(db)
            self.stacked_layout.setCurrentIndex(1)

    def connect_db(self, db: QSqlDatabase, db_username: str, db_password: str):
        db = QSqlDatabase.addDatabase("QPSQL")
        db.setDatabaseName("postgres")
        db.setUserName(db_username)
        db.setPassword(db_password)
        db.setHostName("localhost")
        db.setPort(5432)

        if not db.open():
            print("Failed to connect to database.")
            return 0
        else:
            return 1

    def db_display(self, db: QSqlDatabase) -> None:
        db_page = QWidget()
        layout = QGridLayout()

        layout.addWidget(QLabel("Transactions"), 0, 0)
        layout.addWidget(QLabel("Search:"), 1, 0)
        layout.addWidget(QLineEdit(), 2, 0, 1, 3)

        table = QTableView()

        # default query
        query = QSqlQueryModel()
        query.setQuery(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                age INTEGER NOT NULL
            );
            """,
            db,
        )
        query.setQuery(
            """
            SELECT * FROM users;
            """,
            db,
        )
        table.setModel(query)
        layout.addWidget(table, 3, 0, 1, 3)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        db_page.setLayout(layout)
        self.stacked_layout.addWidget(db_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # with open("styles.qss", "r") as f:
    #     _style = f.read()
    #     app.setStyleSheet(_style)
    window = DBApp()
    app.exec()
