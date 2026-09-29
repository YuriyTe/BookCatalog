from metadata import parse_fb2

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

    for item in folder.rglob("*"):
        if item.is_file() and item.suffix.lower() in BOOK_FORMATS:
            books.append(item)

    return books

def create_book_from_file(file_path):
    new_book = {
        "title": file_path.stem,
        "author": None,
        "publication_year": None,
        "first_publication_year": None,
        "genres": [],
        "annotation": None,
        "language": None,
        "cover": None,
        "isbn": None,
        "path": str(file_path),
        "format": file_path.suffix.lower().lstrip("."),
        "status": "new"
    }

    book_format = file_path.suffix.lower().lstrip(".")

    if book_format == "fb2":
        metadata = parse_fb2(file_path)

        if metadata is not None:
            new_book.update(metadata)

    elif book_format == "epub":
        pass
    elif book_format == "pdf":
        pass
    elif book_format == "mobi":
        pass
    elif book_format == "txt":
        pass
    elif book_format == "djvu":
        pass

    return new_book



