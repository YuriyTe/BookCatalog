import xml.etree.ElementTree as ET
from pathlib import Path
from book_manager import compare_metadata, update_book_data, resolve_conflicts
from database import open_database

FB2_NS = "{http://www.gribuser.ru/xml/fictionbook/2.0}"

def read_fb2(file_path):
    try:
        tree = ET.parse(file_path)

        root = tree.getroot()

    except ET.ParseError:
        return None

    return root

def get_description(root):
    description = root.find(f"{FB2_NS}description")

    if description is None:
        return None
    return description

def get_title_info(description):
    title_info = description.find(f"{FB2_NS}title-info")

    return title_info

def get_title(title_info):
    if title_info is None:
        return None

    book_title = title_info.find(f"{FB2_NS}book-title")

    if book_title is None:
        return None

    return book_title.text

def get_author(title_info):
    if title_info is None:
        return None

    author = title_info.find(f"{FB2_NS}author")

    if author is None:
        return None

    first_name = author.find(f"{FB2_NS}first-name")
    last_name = author.find(f"{FB2_NS}last-name")

    first_name = first_name.text if first_name is not None else ""
    last_name = last_name.text if last_name is not None else ""

    return f"{first_name} {last_name}".strip()

def get_genres(title_info):
    if title_info is None:
        return []

    genres = title_info.findall(f"{FB2_NS}genre")

    return [
        genre.text.lower()
        for genre in genres
        if genre.text
    ]

def get_date(title_info):
    if title_info is None:
        return None

    date = title_info.find(f"{FB2_NS}date")
    if date is None:
        return None

    return date.text

def get_publish_info(description):
    return description.find(f"{FB2_NS}publish-info")

def get_publish_year(publish_info):
    if publish_info is None:
        return None

    year = publish_info.find(f"{FB2_NS}year")

    if year is None:
        return None

    return year.text

def get_isbn(publish_info):
    if publish_info is None:
        return None

    isbn = publish_info.find(f"{FB2_NS}isbn")

    if isbn is None:
        return None

    return isbn.text

def get_language(title_info):
    if title_info is None:
        return None

    language = title_info.find(f"{FB2_NS}lang")

    if language is None:
        return None

    return language.text

def get_annotation(title_info):
    if title_info is None:
        return None

    annotation = title_info.find(f"{FB2_NS}annotation")

    if annotation is None:
        return None

    return annotation

def get_annotation_text(annotation):
    if annotation is None:
        return None

    paragraphs = []

    for paragraph in annotation:
        if paragraph.text:
            text = "".join(paragraph.itertext()).strip()

            if text:
                paragraphs.append(text)

    return "\n".join(paragraphs)

def extract_fb2_metadata(root):
    description = get_description(root)

    if description is None:
        return None

    title_info = get_title_info(description)
    publish_info = get_publish_info(description)

    metadata = {
        "title": get_title(title_info),
        "author": get_author(title_info),
        "genre": get_genres(title_info),
        "year": get_publish_year(publish_info),
        "isbn": get_isbn(publish_info),
        "language": get_language(title_info),
        "annotation": get_annotation_text(
            get_annotation(title_info)
        )
    }

    return metadata

if __name__ == "__main__":
    book_data = open_database()
    book = book_data["books"][0]
    print(book)

    decisions = {
        "author": "replace"
    }

    file_path = Path("D:/_BOOKS_TEST/Sci-Fi/Херберт Фрэнк/Дюна  Хроники Дюны/Дюна.fb2")

    root = read_fb2(file_path)
    print("=========================")

    metadata = extract_fb2_metadata(root)
    print("Метадата: ", metadata)

    print("=========================")

    differences = compare_metadata(book, metadata)

    print("=========================")

    book, conflicts = update_book_data(differences, book)
    print('Конфликты:', conflicts)

    print("=========================")
    print("DECISIONS:", decisions)
    print("CONFLICTS:", conflicts)
    print("BEFORE:", book["author"])

    book = resolve_conflicts(book, differences, decisions)

    print("AFTER:", book["author"])

    print("=========================")

    old_genres = ["sf", "adventure"]
    new_genres = ["sf", "adventure"]

    print("Старые:", old_genres)
    print("Новые:", new_genres)

    for value in new_genres:
        if value not in old_genres:
            old_genres.append(value)

    print("Результат:", old_genres)




