from pathlib import Path
from validation import validate_book


class BookCatalog:
    def __init__(self, book_objects):
        self.books = book_objects

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_book_by_source_path(self, source_path):
        path = Path(source_path)

        for book in self.books:
            book_path = Path(book.source_path)

            if book_path == path:
                return book
        return None

    def add_book(self, new_book):
        if self.books:
            new_id = max(book.book_id for book in self.books) + 1
        else:
            new_id = 1

        new_book.book_id = new_id

        if not validate_book(new_book):
            return None

        self.books.append(new_book)

        return new_book

    def delete_book(self, book_id):
        for i, book in enumerate(self.books):
            if book.book_id == book_id:
                self.books.pop(i)
                break
        else:
            print(f"Книга с id {book_id} не найдена.")

    def find_book(self, word):
        query_words = word.lower().split()
        found_books = []

        for book in self.books:
            book_title_lower = book.title.lower()
            if book.author is None:
                book_author_lower = ""
            else:
                book_author_lower = book.author.lower()

            search_text = book_title_lower + " " + book_author_lower

            if all(word in search_text for word in query_words):
                found_books.append(book)

        return found_books


