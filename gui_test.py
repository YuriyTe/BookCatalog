# ===== Импорты =====
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QMessageBox, QListWidget, QListWidgetItem, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt
from file_operations import open_database, save_database
from book_manager import find_book, delete_books, add_book_gui
# ===== Глобальные переменные =====
selected_book_id = None
selected_item = None

# ===== Работа с GUI (функции) =====
def add_book():
    title = title_edit.text()
    author = author_edit.text()
    genre = genre_edit.text()
    year = year_edit.text()
    path = path_edit.text()
    book_format = format_edit.currentText()

    new_book = add_book_gui(
        book_data, title, author, year, genre, path, book_format
    )
    save_database(book_data)

    QMessageBox.information(
        window,
        "Книга добавлена",
        f"Название: {title}\n"
        f"Автор: {author}\n"
        f"Жанр: {genre}"
    )

    title_edit.clear()
    author_edit.clear()
    genre_edit.clear()
    path_edit.clear()
    format_edit.setCurrentIndex(0)
    year_edit.setValue(2000)

def delete_button_clicked():

    if selected_book_id is None:
        return

    ask_delete(selected_book_id)

def ask_delete(book_id):
    global selected_book_id, selected_item

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
        row = book_list.row(selected_item)
        book_list.takeItem(row)

        save_database(book_data)

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
    selected_book_id = None
    selected_item = None

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

    title_edit.clear()
    author_edit.clear()
    genre_edit.clear()

def book_selected(item):
    global selected_book_id, selected_item
    selected_book_id = item.data(Qt.ItemDataRole.UserRole)

    selected_item = item



# ===== Работа с базой =====
book_data = open_database()

# ===== Создание и внешний вид GUI =====
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Book Catalog")
window.resize(800, 600)

central_widget = QWidget()
layout = QVBoxLayout()

button_add = QPushButton("Добавить книгу")
button_delete = QPushButton("Удалить книгу")
button_find = QPushButton("Найти книгу")
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
year_label = QLabel("Год:")
year_edit = QSpinBox()
year_edit.setRange(1200, 2026)
year_edit.setValue(2000)
layout.addWidget(title_label)
path_label = QLabel("Путь:")
path_edit = QLineEdit()
format_label = QLabel("Формат:")
format_edit = QComboBox()

format_edit.addItems([
"fb2", "epub", "pdf", "mobi", "txt"
])


layout.addWidget(title_label)
layout.addWidget(title_edit)
layout.addWidget(author_label)
layout.addWidget(author_edit)
layout.addWidget(genre_label)
layout.addWidget(genre_edit)

layout.addWidget(year_label)
layout.addWidget(year_edit)
layout.addWidget(path_label)
layout.addWidget(path_edit)
layout.addWidget(format_label)
layout.addWidget(format_edit)


layout.addWidget(book_list)

layout.addStretch()
layout.addWidget(button_add)
layout.addWidget(button_delete)
layout.addWidget(button_find)
layout.setSpacing(10)
layout.setContentsMargins(20, 20, 20, 20)

central_widget.setLayout(layout)
window.setCentralWidget(central_widget)



window.show()
app.exec()