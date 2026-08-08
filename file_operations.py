import json
import sys
from datetime import date

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


def open_database():
    try:
        with open('data/book_db.json', 'r', encoding='utf-8') as file:
            book_data = json.load(file)

    except FileNotFoundError:
        print('Ошибка: Файл не найден!')
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print('Ошибка: Неверный формат JSON!')
        sys.exit(2)
    else:
        if validate_database(book_data):
            return book_data


def close_database(book_data):
        book_data['last_updated'] = date.today().isoformat()
        with open('data/book_db.json', 'w', encoding='utf-8') as file:
            json.dump(book_data, file, indent=4, ensure_ascii=False)


