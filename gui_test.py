import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QMessageBox
)

def add_book():
    title = title_edit.text()
    author = author_edit.text()
    genre = genre_edit.text()

    QMessageBox.information(
        window,
        "Книга",
        f"Название: {title}\n"
        f"Автор: {author}\n"
        f"Жанр: {genre}"
    )

    title_edit.clear()
    author_edit.clear()
    genre_edit.clear()

def delete_button_clicked():
    title = title_edit.text()
    ask_delete(title)

def delete_book():
    print("Delete book")

def ask_delete(title):
    answer = QMessageBox.question(
        window,
        "Удаление книги",
        f"Удалить книгу {title}?"
    )
    if answer == QMessageBox.StandardButton.Yes:
        QMessageBox.information(
            window,
            "Удаление",
            "Книга удалена")
    else:
        QMessageBox.information(
            window,
            "Удаление",
            "Удаление отменено")


def find_book():
    print("Find book")

def print_book():
    print("Print book")



app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Book Catalog")
window.resize(800, 600)

central_widget = QWidget()
layout = QVBoxLayout()

button_add = QPushButton("Добавить книгу")
button_delete = QPushButton("Удалить книгу")
button_find = QPushButton("Найти книгу")
button_print = QPushButton("Напечатать книгу")

button_add.clicked.connect(add_book)
button_delete.clicked.connect(delete_button_clicked)
button_find.clicked.connect(find_book)


title_label = QLabel("Название книги:")
title_edit = QLineEdit()

author_label = QLabel("Автор:")
author_edit = QLineEdit()

genre_label = QLabel("Жанр:")
genre_edit = QLineEdit()

layout.addWidget(title_label)
layout.addWidget(title_edit)
layout.addWidget(author_label)
layout.addWidget(author_edit)
layout.addWidget(genre_label)
layout.addWidget(genre_edit)


layout.addStretch()
layout.addWidget(button_add)
layout.addWidget(button_delete)
layout.addWidget(button_find)
layout.addWidget(button_print)
layout.setSpacing(10)
layout.setContentsMargins(20, 20, 20, 20)

central_widget.setLayout(layout)
window.setCentralWidget(central_widget)



window.show()
app.exec()