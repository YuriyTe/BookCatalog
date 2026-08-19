# ===== Импорты =====
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel,
    QMessageBox, QListWidget, QListWidgetItem, QSpinBox, QComboBox, QSplitter,
    QTreeWidget, QTreeWidgetItem, QFileDialog
)
from PySide6.QtCore import Qt
from file_operations import open_database, save_database
from book_manager import find_book, delete_books, add_book_gui
from pathlib import Path


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

def delete_button_clicked(book_data, form_widgets, book_list):
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

def find_button_clicked(book_data, form_widgets, book_list):
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
    button_delete.clicked.connect(lambda: delete_button_clicked(book_data, form_widgets,
                                                            book_list))
    button_find.clicked.connect(lambda: find_button_clicked(book_data, form_widgets,
                                                            book_list))


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

def tree_item_clicked(item, column, book_data):
    path = item.data(
        0,
        Qt.ItemDataRole.UserRole
    )
    path = Path(path)

    if path.is_dir():
        print("Выбрана папка: ", path)
    elif path.is_file():
        book = find_book_info(path, book_data)

        print("TREE:", book["title"])

        if book:
            show_book_info(book, book_info_widgets)

def show_book_info(book, book_info_widgets):
    print("SHOW:", book["title"])

    book_info_widgets["title"].setText(
        f"Название: {book['title']}"
    )
    book_info_widgets["author"].setText(
        f"Автор: {book['author']}"
    )
    book_info_widgets["genre"].setText(
        f"Жанр: {book['genre']}"
    )
    book_info_widgets["year"].setText(
        f"Год: {book['year']}"
    )
    book_info_widgets["format"].setText(
        f"Формат: {book['format']}"
    )
    book_info_widgets["path"].setText(
        f"Путь: {book['path']}"
    )

def find_book_info(path, book_data):
    print("path: ", path)
    for book in book_data["books"]:
        if Path(book["path"]) == path:
            print("Нашли книгу:")
            print(book["title"])
            print(book["author"])
            return book

def scan_folder(folder, tree_item):
    book_formats = {".fb2", ".epub", ".pdf", ".mobi", ".txt", ".djvu"}
    for item in folder.iterdir():
        if item.is_dir():
            folder_item = QTreeWidgetItem(
                tree_item,
                [item.name]
            )
            folder_item.setData(
                0,
                Qt.ItemDataRole.UserRole,
                str(item)
            )
            scan_folder(item, folder_item)

        elif item.is_file():
            if item.suffix.lower() in book_formats:
                book_item = QTreeWidgetItem(
                    tree_item,
                    [item.name]
                )

                book_item.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    str(item)
                )

def choose_folder():

    folder = QFileDialog.getExistingDirectory(
        window,
        "Выберите папку с книгами"
    )

    if folder:
        folder = Path(folder)
        tree.clear()

        root = QTreeWidgetItem(tree, [folder.name])
        root.setData(
            0,
            Qt.ItemDataRole.UserRole,
            str(folder)
        )

        scan_folder(folder, root)

def create_book_info_panel():
    panel = QWidget()
    layout = QVBoxLayout()
    panel.setLayout(layout)

    title_label = QLabel()
    title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    author_label = QLabel()
    genre_label = QLabel()
    year_label = QLabel()
    format_label = QLabel()
    path_label = QLabel()
    path_label.setWordWrap(True)

    layout.setSpacing(2)
    layout.addWidget(title_label)
    layout.addWidget(author_label)
    layout.addWidget(genre_label)
    layout.addWidget(year_label)
    layout.addWidget(format_label)
    layout.addWidget(path_label)

    layout.addStretch()

    return panel, {
        "title": title_label,
        "author": author_label,
        "genre": genre_label,
        "year": year_label,
        "format": format_label,
        "path": path_label
    }


# ===== Работа с базой =====
book_data = open_database()

# ===== Создание и внешний вид GUI =====
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Book Catalog")
window.resize(1200, 600)

splitter = QSplitter(Qt.Orientation.Horizontal)

main_widget = QWidget()
main_layout = QVBoxLayout()
main_layout.addWidget(splitter)
main_widget.setLayout(main_layout)
window.setCentralWidget(main_widget)

left_panel, form_widgets = create_left_panel()

tree_panel = QWidget()
tree_layout = QVBoxLayout()
tree_panel.setLayout(tree_layout)

button_choose_folder = QPushButton("Выбрать папку")
button_choose_folder.clicked.connect(choose_folder)

tree = QTreeWidget()
tree.setHeaderLabels(["Книги"])

tree_layout.addWidget(button_choose_folder)
tree_layout.addWidget(tree)

tree.itemClicked.connect(lambda item, column: tree_item_clicked(item, column, book_data))

book_info_panel, book_info_widgets = create_book_info_panel()

splitter.addWidget(left_panel)
splitter.addWidget(tree_panel)
splitter.addWidget(book_info_panel)
splitter.setSizes([300, 600, 350])
splitter.setStyleSheet("""
    QSplitter::handle {
        background: #888888; width: 3px;
    }""")

window.show()
app.exec()