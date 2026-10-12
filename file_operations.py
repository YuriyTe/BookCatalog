from pathlib import Path
from metadata import Fb2MetadataParser
from parser_factory import ParserFactory

BOOK_FORMATS = {
    ".fb2",
    ".epub",
    ".pdf",
    ".mobi",
    ".txt",
    ".djvu",
}

parser = Fb2MetadataParser()

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
        "source_path": str(file_path),
        "format": file_path.suffix.lower().lstrip("."),
        "status": "new"
    }

    book_format = file_path.suffix.lower().lstrip(".")
    parser = ParserFactory.create_parser(book_format)

    if parser is not None:
        metadata = parser.parse(file_path)

        if metadata is not None:
            new_book.update(metadata)

    return new_book

def is_book_file_missing(book_file_path):
    if book_file_path == "":
        return False
    if not Path(book_file_path).is_file():
        return True
    return False

def get_book_cover(book_file_path, book_format):
    cover = None
    file_is_missing = False

    if book_file_path == "":
        return cover, file_is_missing
    file_is_missing = is_book_file_missing(book_file_path)
    if file_is_missing:
        return cover, file_is_missing

    parser = ParserFactory.create_parser(book_format)
    if parser is not None:
        cover = parser.get_cover(book_file_path)

    return cover, file_is_missing