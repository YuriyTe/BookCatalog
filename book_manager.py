

def show_menu():
    print('1. Показать книги')
    print('2. Добавить книгу')
    print('3. Удалить книгу')
    print('4. Найти книгу')
    print('0. Выход')
    choice = input('Ваш выбор: ')
    return choice

def menu_delete_books(book_list):
    print_books(book_list)

    while True:
        action = input('Введите номер книги для удаления (0 - отмена): ').strip()
        if not action.isdigit():
            print('Enter the digital code of the book')
            continue
        number = int(action)
        if 0 < number <= len(book_list):
            delete_books(book_list, number)
            print('Книга удалена')
        elif number > len(book_list):
            print('There is no such book')
            break
        elif action == '0':
            break

#Menu for finding the book
def menu_find_book(book_list):
    print_books(book_list)
    while True:
        words = input('Введите часть названия книги (0 - для отмены): ').strip().lower()
        if words == '0':
            break
        if words == '' :
            print('Введите текст для поиска.')
            continue
        else:
            found_books = find_book(book_list, words)
            if found_books:
                for num, book in enumerate(found_books, start=1):
                    print(f'{num}. {book}')
                result = input(f'Это то что вы искали (y/n): ').strip().lower()
                if result == 'y':
                    print('Отправляем книгу в программу для чтения') # For now,
                    # for simplicity
                elif result == 'n':
                    continue
            else:
                print('Книги не найдены.')



# Add books to the library
def add_books(book_list):
    print('Вводите названия в строчке ниже, для окончания ввода введите "стоп"')
    while True:
        title = input('Введи название книги: ').strip()
        if title == '':
            print('Вы не ввели название книги')
        elif title == 'стоп':
            break
        else:
            if duplicates_check(book_list, title):
                book_list.append(title)


def print_books(book_list):
    if not book_list:
        print('List is empty')
        return

    print('=' * 30)
    print(f'В библиотеке {len(book_list)} книг(и)')

    for number, book in enumerate(book_list, start=1):
        print(f'{number:2d}. {book}')

    print('=' * 30)

def delete_books(book_list, number):
    book_list.pop(number-1)

# Check for duplicate books
def duplicates_check(book_list, title):
    title_lower = title.lower()
    for name in book_list:
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
def find_book(book_list, word):
    query_words = word.split()
    found_books = []
    for book in book_list:
        book_lower = book.lower()
        if all(word in book_lower for word in query_words):
            found_books.append(book)
    return found_books

