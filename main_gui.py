# ===== Импорты =====
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel,
    QMessageBox, QListWidget, QListWidgetItem, QSpinBox, QComboBox, QSplitter,
    QFileDialog, QFileSystemModel, QTreeView, QDialog, QRadioButton, QCheckBox,
    QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt, QDir, QSize
from PySide6.QtGui import QIcon, QPixmap, QIntValidator
from book_manager import find_book
from pathlib import Path
from database import open_database, find_book_by_id
from metadata import get_fb2_cover
from process_manager import ProcessManager
from datetime import date

# ===== Константы =====
FIELD_NAMES = {
    "author": "Автор",
    "genres": "Жанр",
    "annotation": "Аннотация",
}

# ===== Классы =====
class BookFormPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.left_layout = QVBoxLayout()
        self.setLayout(self.left_layout)

        self.title_label = QLabel("Название книги:")
        self.title_edit = QLineEdit()
        self.author_label = QLabel("Автор:")
        self.author_edit = QLineEdit()
        self.genre_label = QLabel("Жанр:")
        self.genre_edit = QLineEdit()
        self.year_label = QLabel("Год:")
        self.year_edit = QLineEdit()
        current_year = date.today().year
        self.year_validator = QIntValidator(1200, current_year)
        self.year_edit.setValidator(QIntValidator(self.year_validator))
        self.language_label = QLabel("Язык")
        self.language_edit = QComboBox()
        self.language_edit.addItems(["Русский", "English", "Français",
                                     "Deutsch", "Español"])
        self.language_edit.setEditable(True)

        self.left_layout.addWidget(self.title_label)
        self.left_layout.addWidget(self.title_edit)
        self.left_layout.addWidget(self.author_label)
        self.left_layout.addWidget(self.author_edit)
        self.left_layout.addWidget(self.genre_label)
        self.left_layout.addWidget(self.genre_edit)
        self.left_layout.addWidget(self.year_label)
        self.left_layout.addWidget(self.year_edit)
        self.left_layout.addWidget(self.language_label)
        self.left_layout.addWidget(self.language_edit)

        self.button_add = QPushButton("Добавить книгу")
        self.button_delete = QPushButton("Удалить книгу")
        self.button_find = QPushButton("Найти книгу")
        self.book_list = QListWidget()
        self.book_list.setStyleSheet("""
                QListWidget {border: 1px solid #888;} 
                """)
        self.book_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)

        self.form_widgets = {
            "title": self.title_edit,
            "author": self.author_edit,
            "genres": self.genre_edit,
            "publication_year": self.year_edit,
            "language": self.language_edit,
        }

        self.button_add.clicked.connect(lambda: add_manual_book_clicked(
            self.form_widgets))
        self.button_delete.clicked.connect(lambda: delete_button_clicked(book_data,
                                                                         self.form_widgets,
                                                                         self.book_list,
                                                                         book_shelf,
                                                                         process_manager))
        self.button_find.clicked.connect(lambda: find_button_clicked(book_data,
                                                                     self.form_widgets,
                                                                     self.book_list))

        self.left_layout.addWidget(self.book_list)

        self.left_layout.addStretch()
        self.left_layout.addWidget(self.button_add)
        self.left_layout.addWidget(self.button_delete)
        self.left_layout.addWidget(self.button_find)
        self.left_layout.setSpacing(10)
        self.left_layout.setContentsMargins(10, 10, 10, 10)


# ===== Работа с GUI (функции) =====
def delete_button_clicked(book_data, form_widgets, book_list, book_shelf, process_manager):
    selected_items = book_list.selectedItems()
    selected_widget = book_list

    if not selected_items:
        selected_items = book_shelf.selectedItems()
        selected_widget = book_shelf

    if not selected_items:
        return

    ask_delete(book_data, selected_widget, selected_items,
               form_widgets, book_shelf, process_manager)

def ask_delete(book_data, selected_widget, selected_items,
               form_widgets, book_shelf, process_manager):
    answer = QMessageBox.question(
        window,
        "Удаление книг",
        f"Удалить выбранные книги?\nКоличество: {len(selected_items)}"
    )

    if answer == QMessageBox.StandardButton.Yes:
        for item in selected_items:
            book_id = item.data(Qt.ItemDataRole.UserRole)

            result = process_manager.remove_book(book_id)

            if result is not None:
                row = selected_widget.row(item)
                selected_widget.takeItem(row)

            else:
                QMessageBox.information(
                    window,
                    "Удаление",
                    "Удаление не удалось")

        QMessageBox.information(
            window, f"Удаление",
            "Удаление свершилось")

        refresh_book_shelf(book_data, book_shelf)

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
            f"ID: {book["book_id"]} | {book['title']}"
        )
        item.setData(
            Qt.ItemDataRole.UserRole,
            book["book_id"]
        )
        book_list.addItem(item)

    form_widgets["title"].clear()
    form_widgets["author"].clear()
    form_widgets["genres"].clear()

def tree_item_clicked(index, book_data):
    path = model.filePath(index)
    path = Path(path)

    if path.is_dir():
        print("Выбрана папка: ", path)

    elif path.is_file():
        book = find_book_info(path, book_data)

        if book:
            show_book_info(book, book_info_widgets)

def add_selected_book_to_library(book_data):
    index = tree.currentIndex()
    path = model.filePath(index)
    path = Path(path)
    if not path.is_file():
        return
    result = process_manager.import_book(path)

    if result is not None:
        handle_import_conflicts([result])

    refresh_book_shelf(book_data, book_shelf)

def show_book_info(book, book_info_widgets):

    book_info_widgets["title"].setText(f"Название: {book["title"]}"
    )
    book_info_widgets["author"].setText(f"Автор: {book["author"]}"
    )
    book_info_widgets["genres"].setText(f"Жанр: {book["genres"]}"
    )
    book_info_widgets["annotation"].setText(f"Аннотация: {book['annotation']}")
    book_info_widgets["publication_year"].setText(
        f"Год: {book["publication_year"]}"
    )
    book_info_widgets["format"].setText(
        f"Формат: {book['format']}"
    )
    book_info_widgets["path"].setText(
        f"Путь: {book["path"]}"
    )

def find_book_info(path, book_data):

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
    title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    title_label.setWordWrap(True)
    author_label = QLabel()
    genre_label = QLabel()
    annotation_label = QLabel()
    annotation_label.setWordWrap(True)
    year_label = QLabel()
    format_label = QLabel()
    path_label = QLabel()
    path_label.setWordWrap(True)

    layout.setSpacing(2)
    layout.addWidget(title_label)
    layout.addWidget(author_label)
    layout.addWidget(genre_label)
    layout.addWidget(annotation_label)
    layout.addWidget(year_label)
    layout.addWidget(format_label)
    layout.addWidget(path_label)

    layout.addStretch()

    return panel, {
        "title": title_label,
        "author": author_label,
        "genres": genre_label,
        "annotation": annotation_label,
        "publication_year": year_label,
        "format": format_label,
        "path": path_label
    }

def handle_import_conflicts(results):
    remembered_decisions = {}

    for result in results:
        existing_book, differences, conflict_fields  = result

        current_decisions = handle_conflict(conflict_fields, differences,
                                            remembered_decisions)
        process_manager.apply_conflict_decisions(existing_book,
        differences,current_decisions)

def handle_conflict(conflict_fields, differences, remembered_decisions):
    current_decisions = remembered_decisions.copy()

    for field in conflict_fields:
        if field in current_decisions:
            decision = current_decisions[field]
        else:
            data = differences[field]

            decision, apply_to_all = show_conflict_dialog(
            field,
            data["old"],
            data["new"]
            )
            current_decisions[field] = decision

            if apply_to_all:
                remembered_decisions[field] = decision

    return current_decisions

def add_folder_to_library():

    if window.selected_folder is None:
        print("Папка не выбрана")
        return

    results = process_manager.import_folder(window.selected_folder)

    if results:
        handle_import_conflicts(results)

    window.selected_folder = None

    refresh_book_shelf(book_data, book_shelf)

def show_conflict_dialog(field, old_value, new_value, parent=None):
    field_name = FIELD_NAMES.get(field, field)

    dialog = QDialog(parent)
    dialog.setWindowTitle("Конфликт метаданных")
    dialog.setMinimumWidth(500)
    dialog.setMaximumWidth(700)

    layout = QVBoxLayout(dialog)

    layout.addWidget(QLabel(f"Конфликт: {field_name}"))

    old_text = QTextEdit()
    old_text.setPlainText(str(old_value))
    old_text.setReadOnly(True)
    old_text.setMaximumHeight(120)

    new_text = QTextEdit()
    new_text.setPlainText(str(new_value))
    new_text.setReadOnly(True)
    new_text.setMaximumHeight(120)

    layout.addWidget(QLabel("В базе:"))
    layout.addWidget(old_text)

    layout.addWidget(QLabel("В файле:"))
    layout.addWidget(new_text)

    replace_radio = QRadioButton("Заменить")
    keep_radio = QRadioButton("Оставить")

    layout.addWidget(replace_radio)
    layout.addWidget(keep_radio)

    if field in ("genres", "annotation"):
        add_radio = QRadioButton("Добавить")
        layout.addWidget(add_radio)

    apply_all = QCheckBox("Применять выбранное решение для этого поля")
    layout.addWidget(apply_all)

    button_ok = QPushButton("Применить")
    layout.addWidget(button_ok)

    button_ok.clicked.connect(dialog.accept)

    if dialog.exec():
        apply_to_all = apply_all.isChecked()

        if replace_radio.isChecked():
            return "replace", apply_to_all

        if keep_radio.isChecked():
            return "keep", apply_to_all

        if field in ("genres", "annotation") and add_radio.isChecked():
            return "add", apply_to_all

    return None, False

def load_books_to_shelf(book_data, book_shelf):
    for book in book_data["books"]:
        cover = None

        if book["format"] == "fb2":
            cover = get_fb2_cover(book["path"])

        if cover:
            pixmap = QPixmap()
            pixmap.loadFromData(cover)
            pixmap = pixmap.scaled(
                100,
                150,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        else:
            pixmap = QPixmap(100, 150)
            pixmap.fill(Qt.GlobalColor.lightGray)

        item = QListWidgetItem(
            QIcon(pixmap),
            book["title"]
        )
        item.setData(
            Qt.ItemDataRole.UserRole,
            book["book_id"]
        )

        book_shelf.addItem(item)

def refresh_book_shelf(book_data, book_shelf):
    book_shelf.clear()
    load_books_to_shelf(book_data, book_shelf)

def select_book_from_shelf(item):
    book_id = item.data(Qt.ItemDataRole.UserRole)

    book = find_book_by_id(book_data, book_id)

    if book:
        show_book_info(book, book_info_widgets)

def manual_new_book(form_widgets):
    new_book = {}
    new_book["title"] = form_widgets["title"].text().strip()
    if new_book["title"] == '':
        new_book["title"] = None

    new_book["author"] = form_widgets["author"].text().strip()
    if new_book["author"] == '':
        new_book["author"] = None
    year = form_widgets["publication_year"].text()
    if year == '':
        new_book["publication_year"] = None
    else:
        year = int(year)
        if int(year) < 1200 or int(year) > 2026:
            new_book["publication_year"] = None
        else:
            new_book["publication_year"] = year
    new_book["genres"] = []
    genres = form_widgets["genres"].text().split(",")
    for genre in genres:
        genre = genre.strip()
        if genre:
            new_book["genres"].append(genre)
    new_book["language"] = form_widgets["language"].currentText()
    new_book["isbn"] = None
    new_book["first_publication_year"] = None
    new_book["annotation"] = None
    new_book["cover"] = None
    new_book["path"] = ""
    new_book["format"] = ""
    new_book["status"] = "new"

    return new_book

def add_manual_book_clicked(form_widgets):
    new_book = manual_new_book(form_widgets)
    if new_book["title"] is None:
        QMessageBox.information(window,
            "название",
            "Нет названия книги")
        return
    elif new_book["author"] is None:
        QMessageBox.information(window,
            "автор",
            "Нет имени автора")
        return

    result = process_manager.add_manual_book(new_book)
    if result is not None:
        refresh_book_shelf(book_data, book_shelf)
        form_widgets["title"].clear()
        form_widgets["author"].clear()
        form_widgets["genres"].clear()
        form_widgets["publication_year"].clear()
        form_widgets["language"].clearEditText()

        QMessageBox.information(window,
                                "новая книга", "Новая книга внесена в каталог")


# ===== Работа с базой =====
book_data = open_database()

process_manager = ProcessManager(book_data)
# ===== Создание и внешний вид GUI =====
app = QApplication(sys.argv)

window = QMainWindow()
window.selected_folder = None
window.setWindowTitle("Book Catalog")
window.resize(1000, 600)

splitter = QSplitter(Qt.Orientation.Horizontal)

main_widget = QWidget()
main_layout = QVBoxLayout()
main_layout.addWidget(splitter)
main_widget.setLayout(main_layout)
window.setCentralWidget(main_widget)

left_panel = BookFormPanel()
form_widgets = left_panel.form_widgets

tree_panel = QWidget()
tree_layout = QVBoxLayout()
tree_panel.setLayout(tree_layout)

button_choose_folder = QPushButton("Выбрать папку")
button_choose_folder.clicked.connect(choose_folder)
button_add_folder = QPushButton("Добавить папку в библиотеку")
button_add_folder.clicked.connect(add_folder_to_library)
button_add_book = QPushButton("Добавить книгу в библиотеку")

folder_label = QLabel("Папка не выбрана")

model = QFileSystemModel()

model.setFilter(QDir.Filter.AllDirs |
    QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
)

model.setNameFilters([
    "*.fb2", "*.epub", "*.pdf", "*.mobi", "*.txt", "*.djvu"])

model.setNameFilterDisables(False)

tree = QTreeView()
tree.setModel(model)

tree_layout.addWidget(button_choose_folder)

button_row = QHBoxLayout()
button_row.addWidget(button_add_folder)
button_row.addWidget(button_add_book)
tree_layout.addLayout(button_row)

tree_layout.addWidget(folder_label)

# начало вставки вкладок для дерева и книжной полки
tabs = QTabWidget()

# вкладка дерева
tree_tab = QWidget()
tree_tab_layout = QVBoxLayout(tree_tab)
tree_tab_layout.addWidget(tree)
tree_layout.addWidget(tabs)

# вкладка книг
book_shelf_tab = QWidget()
book_shelf_layout = QVBoxLayout(book_shelf_tab)

book_shelf = QListWidget()
book_shelf_layout.addWidget(book_shelf)
book_shelf.setSelectionMode(
    QListWidget.SelectionMode.ExtendedSelection
)


tabs.addTab(tree_tab, "Дерево")
tabs.addTab(book_shelf_tab, "Книги")

pixmap = QPixmap(100, 150)
pixmap.fill(Qt.GlobalColor.lightGray)

book_shelf.setViewMode(QListWidget.ViewMode.IconMode)
book_shelf.setIconSize(QSize(100, 150))
book_shelf.setGridSize(QSize(115, 175))

book_shelf.setFlow(QListWidget.Flow.LeftToRight)
book_shelf.setWrapping(True)
book_shelf.setMovement(QListWidget.Movement.Static)
book_shelf.setResizeMode(QListWidget.ResizeMode.Adjust)

load_books_to_shelf(book_data, book_shelf)

book_shelf.itemClicked.connect(select_book_from_shelf)

tree.clicked.connect(lambda index: tree_item_clicked(index, book_data))
button_add_book.clicked.connect(lambda: add_selected_book_to_library(book_data))

book_info_panel, book_info_widgets = create_book_info_panel()

splitter.addWidget(left_panel)
splitter.addWidget(tree_panel)
splitter.addWidget(book_info_panel)
splitter.setCollapsible(0, False)
splitter.setCollapsible(2, False)

splitter.setSizes([300, 600, 350])
splitter.setStyleSheet("""
    QSplitter::handle {
        background: #888888; width: 3px;
    }""")
book_info_panel.setMinimumWidth(300)
book_info_panel.setMaximumWidth(400)


window.show()
app.exec()