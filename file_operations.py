import json
import os
from datetime import date

def open_database():
    with open('data/book_db.json', 'r+', encoding='utf-8') as file:
        book_data = json.load(file)
        return book_data



def close_database(book_list):
    with open('data/book_db.json', 'w', encoding='utf-8') as file:
        json.dump(book_list, file, indent=4, ensure_ascii=False)

