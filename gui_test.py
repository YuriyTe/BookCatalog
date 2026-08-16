# ===== Импорты =====
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel,
    QMessageBox, QListWidget, QListWidgetItem, QSpinBox, QComboBox, QSplitter, QTreeWidget
)
from PySide6.QtCore import Qt
from file_operations import open_database, save_database
from book_manager import find_book, delete_books, add_book_gui


# ===== Работа с GUI (функции) =====
def add_book(book_data, form_widgets):

    title = form_widgets["title"].text()
    author = form_widgets["author"].text()
    genre = form_widgets["genre"].text()
    year = form_widgets["year"].value()
    path = form_widgets["path"].text()
    book_format = form_widgets["format"].currentText()

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

    form_widgets["title"].clear()
    form_widgets["author"].clear()
    form_widgets["genre"].clear()
    form_widgets["path"].clear()
    form_widgets["format"].setCurrentIndex(0)
    form_widgets["year"].setValue(2000)

def delete_button_clicked(book_data, book_list, form_widgets):
    selected_item = book_list.currentItem()

    if selected_item is None:
        return
    selected_book_id = selected_item.data(
        Qt.ItemDataRole.UserRole
    )

    ask_delete(book_data,
        book_list,
        selected_item,
        selected_book_id, form_widgets)

def ask_delete(book_data, book_list, selected_item, book_id, form_widgets):

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

    form_widgets["title"].clear()

def find_button_clicked(book_data, book_list, form_widgets):
    word = form_widgets["title"].text()
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

    form_widgets["title"].clear()
    form_widgets["author"].clear()
    form_widgets["genre"].clear()

def create_left_panel():
    left_panel = QWidget()
    left_layout = QVBoxLayout()
    left_panel.setLayout(left_layout)

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
    left_layout.addWidget(title_label)
    path_label = QLabel("Путь:")
    path_edit = QLineEdit()
    format_label = QLabel("Формат:")
    format_edit = QComboBox()

    format_edit.addItems([
        "fb2", "epub", "pdf", "mobi", "txt"
    ])

    left_layout.addWidget(title_label)
    left_layout.addWidget(title_edit)
    left_layout.addWidget(author_label)
    left_layout.addWidget(author_edit)
    left_layout.addWidget(genre_label)
    left_layout.addWidget(genre_edit)

    left_layout.addWidget(year_label)
    left_layout.addWidget(year_edit)
    left_layout.addWidget(path_label)
    left_layout.addWidget(path_edit)
    left_layout.addWidget(format_label)
    left_layout.addWidget(format_edit)

    button_add = QPushButton("Добавить книгу")
    button_delete = QPushButton("Удалить книгу")
    button_find = QPushButton("Найти книгу")
    book_list = QListWidget()
    book_list.setStyleSheet("""
        QListWidget {border: 1px solid #888;} 
        """)

    button_add.clicked.connect(lambda: add_book(book_data, form_widgets))
    button_delete.clicked.connect(lambda: delete_button_clicked(book_data, book_list,
                                                            form_widgets))
    button_find.clicked.connect(lambda: find_button_clicked(book_data, book_list,
                                                            form_widgets))


    left_layout.addWidget(book_list)

    left_layout.addStretch()
    left_layout.addWidget(button_add)
    left_layout.addWidget(button_delete)
    left_layout.addWidget(button_find)
    left_layout.setSpacing(10)
    left_layout.setContentsMargins(20, 20, 20, 20)

    return left_panel, {
        "title": title_edit,
        "author": author_edit,
        "genre": genre_edit,
        "year": year_edit,
        "path": path_edit,
        "format": format_edit
    }


# ===== Работа с базой =====
book_data = open_database()

# ===== Создание и внешний вид GUI =====
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Book Catalog")
window.resize(800, 600)

splitter = QSplitter(Qt.Orientation.Horizontal)

main_widget = QWidget()

main_layout = QVBoxLayout()
main_layout.addWidget(splitter)

main_widget.setLayout(main_layout)
window.setCentralWidget(main_widget)

left_panel, form_widgets = create_left_panel()
right_panel = QWidget()

right_layout = QVBoxLayout()
right_panel.setLayout(right_layout)

splitter.addWidget(left_panel)
splitter.addWidget(right_panel)

splitter.setSizes([250, 550])

label_test = QLabel('Здесь будет основное окно библиотеки')
right_layout.addWidget(label_test)

window.show()
app.exec()