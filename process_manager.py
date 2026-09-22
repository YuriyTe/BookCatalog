from database import find_book_by_id, find_book_by_path, save_database, add_book
from book_manager import delete_books, compare_metadata, process_metadata_differences, resolve_conflicts
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
        book_conflicts = []
        books = scan_folder(folder_path)

        for file_path in books:
            result_import = self.import_book(file_path)
            if result_import is not None:
                book_conflicts.append(result_import)
        if book_conflicts:
            return book_conflicts


    def import_book(self, file_path):
        new_book = create_book_from_file(file_path)
        existing_book = find_book_by_path(self.book_data, file_path)

        if existing_book is not None:
            differences = compare_metadata(existing_book, new_book)
            if not differences:
                return
            existing_book, conflict_fields = process_metadata_differences(differences,
                                                                    existing_book)
            if conflict_fields:
                return existing_book, differences, conflict_fields

            save_database(self.book_data)
        else:
            add_book(self.book_data, new_book)
            save_database(self.book_data)


    def apply_conflict_decisions(self, existing_book, differences, decisions):
        book = resolve_conflicts(existing_book, differences, decisions)
        save_database(self.book_data)
        return book

    def add_manual_book(self, new_book):
        result = add_book(self.book_data, new_book)
        if result is not None:
            save_database(self.book_data)

        return result