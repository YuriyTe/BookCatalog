from database import open_database, save_database
from pathlib import Path

BOOK_FORMATS = {
    ".fb2",
    ".epub",
    ".pdf",
    ".mobi",
    ".txt",
    ".djvu",
}

def scan_folder(folder):
    book_formats = {".fb2", ".epub", ".pdf", ".mobi", ".txt", ".djvu"}
    books = []

    for item in folder.rglob("*"):
        if item.is_file() and item.suffix.lower() in book_formats:
            books.append(item)

    return books

def create_book_from_file(file_path):
    new_book = {
        "title": file_path.stem,
        "author": None,
        "year": None,
        "first_published": None,
        "genre": [],
        "path": str(file_path),
        "format": file_path.suffix.lower().lstrip("."),
        "status": "new"
    }
    return new_book



