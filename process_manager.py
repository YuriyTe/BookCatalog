from pathlib import Path

from book import Book
from database import save_database, catalog_to_database_data
from book_manager import compare_metadata, process_metadata_differences, resolve_conflicts
from file_operations import scan_folder, create_book_from_file


class ProcessManager:
    def __init__(self, book_catalog):
        self.book_catalog = book_catalog

    def remove_book(self, book_id):
        book = self.book_catalog.find_book_by_id(book_id)
        if book is None:
            return None

        self.book_catalog.delete_book(book_id)
        data_to_save = catalog_to_database_data(self.book_catalog)
        save_database(data_to_save)

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
        existing_book = self.book_catalog.find_book_by_source_path(file_path)

        if existing_book is not None:
            differences = compare_metadata(existing_book, new_book)
            if not differences:
                return
            existing_book, conflict_fields = process_metadata_differences(differences,
                                                                    existing_book)
            if conflict_fields:
                return existing_book, differences, conflict_fields

            data_to_save = catalog_to_database_data(self.book_catalog)
            save_database(data_to_save)
        else:
            new_book = Book(new_book)
            self.book_catalog.add_book(new_book)

            data_to_save = catalog_to_database_data(self.book_catalog)
            save_database(data_to_save)

    def apply_conflict_decisions(self, existing_book, differences, decisions):
        book = resolve_conflicts(existing_book, differences, decisions)

        data_to_save = catalog_to_database_data(self.book_catalog)
        save_database(data_to_save)
        return book

    def add_manual_book(self, new_book):
        new_book = Book(new_book)
        result = self.book_catalog.add_book(new_book)
        if result is not None:
            data_to_save = catalog_to_database_data(self.book_catalog)
            save_database(data_to_save)

        return result

    def manual_update_book(self, book_id, changed_book):
        book = self.book_catalog.find_book_by_id(book_id)
        if book is None:
            return
        book.title = changed_book["title"]
        book.author = changed_book["author"]
        book.genres = changed_book["genres"]
        book.publication_year = changed_book["publication_year"]
        book.language = changed_book["language"]

        data_to_save = catalog_to_database_data(self.book_catalog)
        save_database(data_to_save)
        return book

    def update_source_path(self, book_id, new_source_path):
        book = self.book_catalog.find_book_by_id(book_id)
        if book is None:
            return None, "book_not_found"

        source_path = Path(new_source_path)
        new_path_format = source_path.suffix.lower().lstrip(".")
        if new_path_format != book.format:
            return None, "wrong_format"
        else:
            book.source_path = new_source_path

            data_to_save = catalog_to_database_data(self.book_catalog)
            save_database(data_to_save)
            return book, None
