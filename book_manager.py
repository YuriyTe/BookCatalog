

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
            print('Книга удалена')
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
                for num, book in enumerate(found_books, start=1):
                    print(f'{num}. {book}')
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

    while True:
        title = input('Введи название книги: ').strip()
        if title == '':
            print('Вы не ввели название книги')
        elif title.lower() == 'стоп':
            return
        else:
            added_book["title"] = title
            break

    while True:
        author = input('Введи Имя и фамилию автора: ').strip()
        if author == '':
            print('Вы не ввели имя автора')
        elif author.lower() == 'стоп':
            return
        else:
            added_book["author"] = author
            break

    while True:
        year = input('Введи год издания: ').strip()
        if year == '':
            print('Вы не ввели год издания')
        elif year.lower() == 'стоп':
            return
        else:
            added_book["year"] = year
            break

    while True:
        genre = input('Введи жанр книги: ').strip()
        if genre == '':
            print('Вы не ввели жанр')
        elif genre.lower() == 'стоп':
            return
        else:
            added_book["genre"].append(genre)
            break

    while True:
        path = input('Ввести путь к книге').strip()
        if path == '':
            print('Вы не ввели путь к книге')
        elif path.lower() == 'стоп':
            break
        else:
            added_book["path"] = path
            break

    book_data["books"].append(added_book)
    print(f"Книга '{added_book['title']}' добавлена (ID: {added_book['id']})")



def print_books(book_data):
    if not book_data:
        print('List is empty')
        return

    print('=' * 30)
    print(f'В библиотеке {len(book_data["books"])} книг(и)')

    for book in (book_data["books"]):
        print(f'{book["id"]}. {book["title"]} — {book["author"]}')

    print('=' * 30)


def delete_books(book_data, id_number):
    for i, book in enumerate(book_data["books"]):
        if book["id"] == id_number:
            deleted_book = book_data["books"].pop(i)
            print((f"Удалена книга: {deleted_book['title']} ({deleted_book['author']})"))
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

#
def find_book(book_data, word):
    query_words = word.split()
    found_books = []
    for book in book_data:
        book_lower = book.lower()
        if all(word in book_lower for word in query_words):
            found_books.append(book)
    return found_books

