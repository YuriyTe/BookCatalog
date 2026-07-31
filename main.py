"""
BookCatalog, Главный файл программы
версия 0.0.1
"""

from book_manager import print_books, add_books, show_menu

book_list = []
while True:
    choice = show_menu()

    if choice == '1':
        print_books(book_list)
    elif choice == '2':
        add_books(book_list)
    elif choice == '0':
        break
