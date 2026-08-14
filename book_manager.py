from file_operations import save_database
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
                    print(f'{book["id"]}. {book["title"]} - {book["author"]}')
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
    max_id = max((book.get("id", 0) for book in book_data["books"]), default=0)
    added_book = {
      "id": max_id + 1,
      "title": "",
      "author": "",
      "year": 0,
      "genre": [],
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
    added_book["year"] =   year

    genre = input_required('Введи жанр, (если больше одного, через запятую)')
    if genre is None:
        return
    genre = [g.strip() for g in genre.split(',') if g.strip()]
    added_book["genre"] =  genre

    path = input_required('Введи путь к директории')
    if path is None:
        return
    added_book["path"] = path


    book_data["books"].append(added_book)
    book_data["book_count"] = len(book_data["books"])
    print(f"Книга '{added_book["title"]}' добавлена (ID: {added_book["id"]})")

def add_book_gui(book_data, title, author, year, genre, path, book_format):
    if book_data["books"]:
        new_id = max(book["id"] for book in book_data["books"]) + 1
    else:
        new_id = 1
    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "path": path,
        "format": book_format
    }
    book_data["books"].append(new_book)
    return new_book

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
        print(f'{book["id"]}. {title} — {author}')

    print('=' * 30)


def delete_books(book_data, id_number):
    for i, book in enumerate(book_data["books"]):
        if book["id"] == id_number:
            deleted_book = book_data["books"].pop(i)

            break
    else:
        print(f"Книга с id {id_number} не найдена.")

# Check for duplicate books
def duplicates_check(book_data, title):
    title_lower = title.lower()
    for name in book_data:
        if title_lower == name.lower():
            print('Такая книга уже есть')
            action = input('Добавить еще один экземпляр? (y/n): ').strip().lower()
            if action == 'y':
                return True
            elif action == 'n':
                return False
            else:
                return False
    return True


def find_book(book_data, word):
    query_words = word.lower().split()
    found_books = []
    for book in book_data["books"]:
        book_lower = book["title"].lower()
        if all(word in book_lower for word in query_words):
            found_books.append(book)

    return found_books

