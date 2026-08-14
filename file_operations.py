import json
import sys
from datetime import date
from validation import validate_database



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


def save_database(book_data):
        book_data['last_updated'] = date.today().isoformat()
        with open('data/book_db.json', 'w', encoding='utf-8') as file:
            json.dump(book_data, file, indent=4, ensure_ascii=False)


