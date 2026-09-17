from database import find_book_by_id, find_book_by_path, save_database, add_book
from book_manager import delete_books
from file_operations import scan_folder, create_book_from_file


class ProcessManager:
    def __init__(self, book_data):
        self.book_data = book_data

    def remove_book(self, book_id):
        book = find_book_by_id(self.book_data, book_id)
        if book is None:
            return None

        delete_books(self.book_data, book_id)
        save_database(self.book_data)
        print(f'Book {book["title"]} removed')

        return book


    def import_folder(self, folder_path):

        books = scan_folder(folder_path)

        for file_path in books:
            existing_book = find_book_by_path(self.book_data, file_path)

            if existing_book is not None:
                continue

            new_book = create_book_from_file(file_path)
            add_book(self.book_data, new_book)

        save_database(self.book_data)
