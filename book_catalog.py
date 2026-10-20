from pathlib import Path
from validation import validate_book


class BookCatalog:
    def __init__(self, book_data):
        self.book_data = book_data

    def find_book_by_id(self, book_id):
        for book in self.book_data["books"]:
            if book["book_id"] == book_id:
                return book
        return None

    def find_book_by_source_path(self, source_path):
        path = Path(source_path)

        for book in self.book_data["books"]:
            book_path = Path(book["source_path"])

            if book_path == path:
                return book
        return None

    def add_book(self, new_book):
        if self.book_data["books"]:
            new_id = max(book["book_id"] for book in self.book_data["books"]) + 1
        else:
            new_id = 1

        new_book["book_id"] = new_id

        if not validate_book(new_book):
            return None

        self.book_data["books"].append(new_book)
        self.book_data["book_count"] = len(self.book_data["books"])

        return new_book

    def delete_book(self, book_id):
        for i, book in enumerate(self.book_data["books"]):
            if book["book_id"] == book_id:
                self.book_data["books"].pop(i)
                self.book_data["book_count"] = len(self.book_data["books"])
                break
        else:
            print(f"Книга с id {book_id} не найдена.")