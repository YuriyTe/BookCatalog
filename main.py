"""
BookCatalog, Главный файл программы
"""
from book_manager import (print_books, add_books, show_menu, menu_delete_books,
                          menu_find_book)
from config import DEBUG, TEST_BOOKS, VERSION

print(f"BookCatalog {VERSION}")

if DEBUG:
    book_list = TEST_BOOKS.copy()
else:
    book_list = []


while True:
    choice = show_menu()

    if choice == '1':
        print_books(book_list)
    elif choice == '2':
        add_books(book_list)
    elif choice == '3':
        menu_delete_books(book_list)
    elif choice == '4':
        menu_find_book(book_list)
    elif choice == '0':
        break
