import sys


def validate_database(book_data):
    if not isinstance(book_data, dict):
        print('Ошибка: формат записи нарушен JSON!')
        sys.exit(3)
    elif not all(key in book_data for key in ('last_updated', 'book_count', 'books')):
        print('Ошибка: Не хватает данных в файле JSON!')
        sys.exit(4)
    elif not isinstance(book_data['books'], list):
        print('Ошибка: Нет записей книг в библиотеке!')
        sys.exit(5)
    for item in book_data['books']:
        if not isinstance(item, dict):
            print('Ошибка: Нарушен фармат записи данных о книге!')
            sys.exit(6)
    return True

def validate_book(book):
    required_keys = (
        'id', 'title', 'author', 'year', 'genre', 'path','format'
    )
    title = book.get('title', 'отсутствует ключ title')
    genre = book.get('genre', 'нет ключа genre')
    int_keys =['id', 'year']
    string_keys =['title', 'author', 'path', 'format']
    for key in required_keys:
        if key not in book:
            print(f'Ключ {key} отсутствует в описании книги {title}!')

    if key in int_keys:
        if key in book and not isinstance(book[key], int):
            print(f'Проверить правильность введёного {key} в книге {title}!')

    if key in string_keys:
        if key in book and not isinstance(book[key], str):
            print(f'Проверить формат ввденых строковых данных по ключу {key} в книге'
                  f' {title}')
    if not isinstance(genre, list):
        print(f'Проверить формат введённого списка жанров в книге {title}')
    else:
        for item in genre:
            if not isinstance(item, str):
                print(f'Проверить правильность введёных названий жанров в книге {title}')
