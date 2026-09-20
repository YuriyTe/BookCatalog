
from validation import validate_book

def show_menu():
    print('1. Показать книги')
    print('2. Добавить книгу')
    print('3. Удалить книгу')
    print('4. Найти книгу')
    print('0. Выход')
    choice = input('Ваш выбор: ')
    return choice

def menu_delete_books(book_data):
    print_books(book_data)

    while True:
        action = input('Введите ID книги для удаления (0 - отмена): ').strip()
        if not action.isdigit():
            print('Enter the digital code of the book')
            continue
        number = int(action)
        if 0 < number <= len(book_data["books"]):
            delete_books(book_data, number)
        elif number > len(book_data["books"]):
            print('There is no such book')
            break
        elif action == '0':
            break

#Menu for finding the book
def menu_find_book(book_data):
    print_books(book_data)
    while True:
        words = input('Введите часть названия книги (0 - для отмены): ').strip().lower()
        if words == '0':
            break
        if words == '' :
            print('Введите текст для поиска.')
        else:
            found_books = find_book(book_data, words)
            if found_books:
                for book in (found_books):
                    print(f'{book["book_id"]}. {book["title"]} - {book["author"]}')
                result = input('Это то что вы искали (y/n): ').strip().lower()
                if result == 'y':
                    print('Отправляем книгу в программу для чтения') # For now,
                    # for simplicity
                elif result == 'n':
                    continue
            else:
                print('Книги не найдены.')

# Add books to the library
def add_books(book_data):
    max_id = max((book.get("book_id", 0) for book in book_data["books"]), default=0)
    added_book = {
      "book_id": max_id + 1,
      "title": "",
      "author": "",
      "publication_year": 0,
      "genres": [],
      "path": "",
      "format": "fb2"
    }
    print('Вводите данные, для окончания ввода "стоп"')

    title = input_required('Введи название книги: ')
    if title is None:
        return
    added_book["title"] = title

    author = input_required('Введи Имя и фамилию автора')
    if author is None:
        return
    added_book["author"] = author

    year = input_year('Введи год издания')
    if year is None:
        return
    added_book["publication_year"] =   year

    genre = input_required('Введи жанр, (если больше одного, через запятую)')
    if genre is None:
        return
    genre = [g.strip() for g in genre.split(',') if g.strip()]
    added_book["genres"] =  genre

    path = input_required('Введи путь к директории')
    if path is None:
        return
    added_book["path"] = path

    book_data["books"].append(added_book)
    book_data["book_count"] = len(book_data["books"])

def input_required(message):
    while True:
        value = input(f'{message}: ').strip()
        if value == '':
            print('Поле не может быть пустым.')
        elif value.lower() == 'стоп':
            return None
        else:
            return value

def input_year(message):
    while True:
        value = input(message).strip()
        if value.lower() == "стоп":
            return None
        if not value.isdigit():
            print("Введите число.")
            continue

        return int(value)

def print_books(book_data):
    if not book_data:
        print('List is empty')
        return

    print('=' * 30)
    print(f'В библиотеке {len(book_data["books"])} книг(и)')

    for book in (book_data["books"]):
        validate_book(book)
        title = book.get("title", "Нет названия")
        author = book.get("author", "нет имени автора")
        print(f'{book["book_id"]}. {title} — {author}')

    print('=' * 30)

def delete_books(book_data, id_number):
    for i, book in enumerate(book_data["books"]):
        if book["book_id"] == id_number:
            deleted_book = book_data["books"].pop(i)
            book_data["book_count"] = len(book_data["books"])
            break
    else:
        print(f"Книга с id {id_number} не найдена.")

def find_book(book_data, word):
    query_words = word.lower().split()
    found_books = []
    for book in book_data["books"]:
        book_lower = book["title"].lower()
        if all(word in book_lower for word in query_words):
            found_books.append(book)

    return found_books

def compare_metadata(book, metadata):
    differences = {}

    for key, new_value in metadata.items():
        if key == "path":
            continue

        old_value = book.get(key)

        if old_value != new_value:
            differences[key] = {
                "old": old_value,
                "new": new_value,
                "empty": is_empty_value(old_value)
            }

    return differences

def is_empty_value(value):
    return value is None or value == "" or value == []

def process_metadata_differences(differences, book):
    conflict_fields = []

    for field, data in differences.items():
        if data["empty"]:
            book[field] = data["new"]
        else:
            conflict_fields.append(field)
    return book, conflict_fields

def resolve_conflicts(book, differences, decisions):
    for field, data in differences.items():
        if data["empty"]:
            continue
        decision = decisions.get(field)


        if decision == "replace":
            book[field] = data["new"]

        elif decision == "keep":
            continue
        elif decision == "add" and field == "genres":
            book[field] = add_unique_values(book[field], data["new"])
        elif decision == "add" and field == "annotation":
            book[field] = book[field] + "\n\n" + data["new"]

    return book

def add_unique_values(old_values, new_values):
    for value in new_values:
        if value not in old_values:
            old_values.append(value)

    return old_values

