import sys


def validate_database(book_data):
    if not isinstance(book_data, dict):
        return False

    required_keys = {
        "last_updated",
        "book_count",
        "books",
    }

    if not required_keys.issubset(book_data.keys()):
        return False

    if not isinstance(book_data["last_updated"], str):
        return False

    if not isinstance(book_data["book_count"], int):
        return False

    if not isinstance(book_data["books"], list):
        return False

    if book_data["book_count"] != len(book_data["books"]):
        return False

    for book in book_data["books"]:
        if not validate_book(book):
            return False

    return True

def validate_book(book):
    if not isinstance(book, dict):
        return False

    required_keys = {
        "id",
        "title",
        "author",
        "year",
        "first_published",
        "genre",
        "path",
        "format",
        "status",
    }
    if not required_keys.issubset(book.keys()):
        return False

    if not isinstance(book["id"], int):
        return False

    if not isinstance(book["title"], str):
        return False

    if book["author"] is not None and not isinstance(book["author"], str):
        return False

    if book["year"] is not None and not isinstance(book["year"], int):
        return False

    if (
            book["first_published"] is not None
            and not isinstance(book["first_published"], int)
    ):
        return False
    if not isinstance(book["genre"], list):
        return False

    if not all(isinstance(genre, str) for genre in book["genre"]):
        return False

    if not isinstance(book["path"], str):
        return False

    if not isinstance(book["format"], str):
        return False

    if not isinstance(book["status"], str):
        return False

    return True


