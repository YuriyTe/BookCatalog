

def show_menu():
    print('1. Показать книги')
    print('2. Добавить книгу')
    print('3. Удалить книгу')
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


def add_books(book_list):
    print('Вводите названия в строчке ниже, для окончания ввода введите "стоп"')
    while True:
        name = input('Введи название книги: ').strip()
        if name == '':
            print('Вы не ввели название книги')
        elif name == 'стоп':
            break
        else:
            book_list.append(name)


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




