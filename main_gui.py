# ===== Импорты =====
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel,
    QMessageBox, QListWidget, QListWidgetItem, QSpinBox, QComboBox, QSplitter,
    QFileDialog, QFileSystemModel, QTreeView
)
from PySide6.QtCore import Qt, QDir
from book_manager import find_book, delete_books, compare_metadata
from pathlib import Path
from file_operations import scan_folder, create_book_from_file
from database import open_database, save_database, find_book_by_path, add_book
from book_manager import update_book_data


# ===== Работа с GUI (функции) =====
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

    #button_add.clicked.connect(lambda: add_book(book_data, form_widgets))
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

def tree_item_clicked(index, book_data):
    path = model.filePath(index)
    path = Path(path)

    if path.is_dir():
        print("Выбрана папка: ", path)

    elif path.is_file():
        book = find_book_info(path, book_data)

        if book:
            show_book_info(book, book_info_widgets)

def show_book_info(book, book_info_widgets):
    print("SHOW_name in show_book_info:", book["title"])

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
    print("Найденный путь: ", path)

    for book in book_data["books"]:
        if Path(book["path"]) == path:
            print("Нашли книгу:")
            print("Нашли название: ", book["title"])
            print("Нашли автора", book["author"])
            return book
    return None

def choose_folder():
    folder = QFileDialog.getExistingDirectory(
        window,
"Выберите папку с книгами")

    if folder:
        window.selected_folder = Path(folder)

        folder_label.setText(
            f"📁 {window.selected_folder.name}"
        )

        root_path = model.setRootPath(folder)
        tree.setRootIndex(root_path)

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

def update_existing_book(existing_book, file_path):
    new_book = create_book_from_file(file_path)

    differences = compare_metadata(existing_book, new_book)

    if not differences:
        return
    existing_book, conflicts = update_book_data(differences, existing_book)

    if conflicts:
        print("Конфликты:", conflicts)


def add_folder_to_library():
    if not hasattr(window, "selected_folder"):
        print("Папка не выбрана")
        return

    books = scan_folder(window.selected_folder)

    for file_path in books:
        existing_book = find_book_by_path(book_data, file_path)

        if existing_book:
            update_existing_book(existing_book, file_path)
            continue

        new_book = create_book_from_file(file_path)
        add_book(book_data, new_book)

        print(f"Добавлена: {file_path}")

    save_database(book_data)

# ===== Работа с базой =====
book_data = open_database()

# ===== Создание и внешний вид GUI =====
app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("Book Catalog")
window.resize(1000, 600)

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
button_add_folder = QPushButton("Добавить открытую папку в библиотеку")
button_add_folder.clicked.connect(add_folder_to_library)

folder_label = QLabel("Папка не выбрана")

model = QFileSystemModel()

model.setFilter(
    QDir.Filter.AllDirs |
    QDir.Filter.Files |
    QDir.Filter.NoDotAndDotDot
)

model.setNameFilters([
    "*.fb2", "*.epub", "*.pdf", "*.mobi", "*.txt", "*.djvu"])

model.setNameFilterDisables(False)

tree = QTreeView()
tree.setModel(model)


tree_layout.addWidget(button_choose_folder)
tree_layout.addWidget(button_add_folder)
tree_layout.addWidget(folder_label)
tree_layout.addWidget(tree)

tree.clicked.connect(lambda index: tree_item_clicked(index, book_data))

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