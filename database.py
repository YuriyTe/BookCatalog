import json
import sys
from datetime import date
from validation import validate_database, validate_book
from pathlib import Path


def open_database():
    try:
        with open('data/book_db.json', 'r', encoding='utf-8') as file:
            book_data = json.load(file)

    except FileNotFoundError:
        print("Ошибка: файл базы данных не найден!")
        return None

    except json.decoder.JSONDecodeError:
        print("Ошибка: файл базы данных содержит некорректный JSON!")
        return None

    if not validate_database(book_data):
        print("Ошибка: структура базы данных нарушена!")
        return None

    return book_data

def save_database(book_data):
    book_data['last_updated'] = date.today().isoformat()
    with open('data/book_db.json', 'w', encoding='utf-8') as file:
        json.dump(book_data, file, indent=4, ensure_ascii=False)

def add_book(book_data, new_book):
    if book_data["books"]:
        new_id = max(book["id"] for book in book_data["books"]) + 1
    else:
        new_id = 1

    new_book["id"] = new_id

    if not validate_book(new_book):
        return None

    book_data["books"].append(new_book)
    book_data["book_count"] = len(book_data["books"])

    return new_book

def find_book_by_path(book_data, path):
    path = Path(path)

    for book in book_data["books"]:
        book_path = Path(book["path"])

        if book_path == path:
            return book

    return None