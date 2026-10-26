import json
from datetime import date

from book_catalog import BookCatalog
from validation import validate_database
from book import Book


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

def book_data_to_objects(book_data):
    book_objects = []
    for book_record in book_data["books"]:
        book = Book(book_record)
        book_objects.append(book)
    return book_objects

def catalog_to_records(book_catalog):
    book_data = []
    for book in book_catalog.books:
        book_record = vars(book)
        book_data.append(book_record)
    return book_data

def catalog_to_database_data(book_catalog):
    data_to_save = {}
    data_to_save["book_count"] = len(book_catalog.books)
    records = catalog_to_records(book_catalog)
    data_to_save["books"] = records
    return data_to_save

def save_database(book_data):
    book_data['last_updated'] = date.today().isoformat()
    with open('data/book_db.json', 'w', encoding='utf-8') as file:
        json.dump(book_data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    book_data = open_database()
    book_objects = book_data_to_objects(book_data)
    book_catalog = BookCatalog(book_objects)

    data_to_save = {}
    data_to_save["book_count"] = len(book_catalog.books)
    records = catalog_to_records(book_catalog)
    data_to_save["books"] = records
    save_database(data_to_save)








