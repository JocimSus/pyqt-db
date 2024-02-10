import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTableView,
)
from PySide6.QtSql import QSqlDatabase, QSqlQueryModel


class DBWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Interface DB")
        self.resize(800, 600)

        self.db_display()
        self.show()

    def db_display(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        layout.addWidget(QLabel("Transactions"), 0, 0)
        layout.addWidget(QLabel("Search:"), 1, 0)
        layout.addWidget(QLineEdit(), 2, 0, 1, 3)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        db = QSqlDatabase.addDatabase("QPSQL")
        db.setDatabaseName("postgres")
        db.setUserName("postgres")
        db.setPassword("admin10110")
        db.setHostName("localhost")
        db.setPort(5432)

        if not db.open():
            print("Failed to connect to database.")
            return

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    window = DBWindow()
    app.exec()
