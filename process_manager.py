from pathlib import Path

from database import save_database
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
        book_data = self.book_catalog.book_data
        save_database(book_data)

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

            book_data = self.book_catalog.book_data
            save_database(book_data)
        else:
            self.book_catalog.add_book(new_book)

            book_data = self.book_catalog.book_data
            save_database(book_data)

    def apply_conflict_decisions(self, existing_book, differences, decisions):
        book = resolve_conflicts(existing_book, differences, decisions)

        book_data = self.book_catalog.book_data
        save_database(book_data)
        return book

    def add_manual_book(self, new_book):
        result = self.book_catalog.add_book(new_book)
        if result is not None:
            book_data = self.book_catalog.book_data
            save_database(book_data)

        return result

    def manual_update_book(self, book_id, new_data):
        book = self.book_catalog.find_book_by_id(book_id)
        if book is None:
            return
        book["title"] = new_data["title"]
        book["author"] = new_data["author"]
        book["genres"] = new_data["genres"]
        book["publication_year"] = new_data["publication_year"]
        book["language"] = new_data["language"]

        book_data = self.book_catalog.book_data
        save_database(book_data)
        return book

    def update_source_path(self, book_id, new_source_path):
        book = self.book_catalog.find_book_by_id(book_id)
        if book is None:
            return None, "book_not_found"

        source_path = Path(new_source_path)
        new_path_format = source_path.suffix.lower().lstrip(".")
        if new_path_format != book["format"]:
            return None, "wrong_format"
        else:
            book["source_path"] = new_source_path
            book_data = self.book_catalog.book_data
            save_database(book_data)
            return book, None
