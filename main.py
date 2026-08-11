"""
BookCatalog, Главный файл программы
"""
from book_manager import (print_books, add_books, show_menu, menu_delete_books,
                          menu_find_book)
from config import DEBUG, TEST_BOOKS, VERSION
from file_operations import open_database, close_database
import json


print(f"BookCatalog {VERSION}")

if DEBUG:
    book_data = TEST_BOOKS.copy()
else:
    book_data = open_database()


while True:
    choice = show_menu()

    if choice == '1':
        print_books(book_data)
    elif choice == '2':
        add_books(book_data)
    elif choice == '3':
        menu_delete_books(book_data)
    elif choice == '4':
        menu_find_book(book_data)
    elif choice == '0':
        close_database(book_data)
        break
