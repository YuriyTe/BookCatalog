import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QMessageBox, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from file_operations import open_database, close_database
from book_manager import find_book, delete_books

selected_book_id = None

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
    print("Нажата кнопка удаления")
    print("selected_book_id:", selected_book_id)
    if selected_book_id is None:
        return

    ask_delete(selected_book_id)


def ask_delete(book_id):
    for book in book_data["books"]:
        if book["id"] == book_id:
            title = book["title"]
            break

    answer = QMessageBox.question(
        window,
        "Удаление книги",
        f"Удалить книгу с ID: {book_id}\n«{title}»?"

    )
    if answer == QMessageBox.StandardButton.Yes:
        delete_books(book_data, book_id)

        QMessageBox.information(
            window,
            "Удаление",
            "Книга удалена")
    else:
        QMessageBox.information(
            window,
            "Удаление",
            "Удаление отменено")

    title_edit.clear()


def find_button_clicked():
    word = title_edit.text()
    found_books = find_book(book_data, word)

    book_list.clear()
    for book in found_books:
        item = QListWidgetItem(
            f"ID: {book['id']} | {book['title']}"
        )
        item.setData(
            Qt.ItemDataRole.UserRole,
            book["id"]
        )
        book_list.addItem(item)

    # <editor-fold desc="Показ QMessageBox с книгами">
    # if found_books:
    #     result = ""
    #     for book in found_books:
    #         result += (
    #             f"Название: {book['title']}\n"
    #             f"Автор: {book['author']}\n"
    #             f"Год: {book['year']}\n\n"
    #         )
    #
    #     QMessageBox.information(
    #         window,
    #         "Результат поиска",
    #         result
    #     )
    # else:
    #     QMessageBox.information(
    #         window,
    #         "Результат поиска",
    #         "Книга не найдена"
    #     )
    # </editor-fold>

    title_edit.clear()
    author_edit.clear()
    genre_edit.clear()

def book_selected(item):
    global selected_book_id
    selected_book_id = item.data(Qt.ItemDataRole.UserRole)

    print("Выбрана книга:", selected_book_id)

def print_book():
    print("Print book")


book_data = open_database()
print(f'Книг в списке {len(book_data["books"])}')

for book in book_data["books"]:
    print(book["title"])


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
book_list = QListWidget()
book_list.setStyleSheet("""
    QListWidget {
        border: 1px solid #888;
    } """)


button_add.clicked.connect(add_book)
button_delete.clicked.connect(delete_button_clicked)
button_find.clicked.connect(find_button_clicked)
book_list.itemClicked.connect(book_selected)

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

layout.addWidget(book_list)

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