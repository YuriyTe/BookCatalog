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
    books = []

    for item in folder.iterdir():
        if item.is_dir():
            books.extend(scan_folder(item))

        elif item.is_file():
            if item.suffix.lower() in BOOK_FORMATS:
                books.append(item)

    return books




