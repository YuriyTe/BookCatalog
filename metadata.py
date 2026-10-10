# ===== Импорты =====
import xml.etree.ElementTree as ET, base64
from abc import ABC, abstractmethod
from zipfile import ZipFile
from pathlib import PurePosixPath, PurePath

# ===== Константы =====
FB2_NS = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
CONTAINER_NS = "{urn:oasis:names:tc:opendocument:xmlns:container}"
Dublin_Core_NS = "{http://purl.org/dc/elements/1.1/}"
OPF_NS = "{http://www.idpf.org/2007/opf}"

# ===== Классы =====
class MetadataParser(ABC):

    @abstractmethod
    def parse(self, file_path):
        pass

    @abstractmethod
    def get_cover(self, file_path):
        pass

    def normalize_isbn(self, value):
        if value is None:
            return None
        value = str(value)
        value = value.lower()
        value = value.strip()
        value = value.removeprefix("isbn:")
        value = value.removeprefix("urn:")
        value = value.removeprefix("isbn")
        value = value.removeprefix("urnisbn")
        value = value.removeprefix(":")
        value = value.replace("-", "")
        value = value.removeprefix("p:")

        return value.upper()

    def is_valid_isbn(self, value):
        value = str(value)
        if len(value) == 10:
            if value[:9].isdigit() and (value[-1].isdigit() or value[-1] == "X"):
                total = 0
                number = value[:-1]
                for x in range(10, 1, -1):
                    index = 10 - x
                    num = int(number[index]) * x
                    total += num
                if value[-1] == "X":
                    last_num = 10
                else:
                    last_num = int(value[-1])
                total = total + last_num
                if total % 11 == 0:
                    return True

        elif len(value) == 13 and value.isdigit():
            total = 0
            number = value[:-1]
            for index, num in enumerate(number):
                num = int(num)
                if index % 2 == 0:
                    num = num * 1
                else:
                    num = num * 3
                total += num
            check_digit = (10 - total % 10) % 10
            if check_digit == int(value[-1]):
                return True

        return False

class EpubMetadataParser(MetadataParser):
    def parse(self, file_path):
        with ZipFile(file_path, 'r') as zip_file:
            meta_inf = zip_file.read("META-INF/container.xml")
            opf_path = self.get_opf_path(meta_inf)
            if opf_path is None:
                return None

            metadata = self.extract_epub_metadata(zip_file, opf_path)

        return metadata

    def get_cover(self, file_path):
        with ZipFile(file_path, 'r') as zip_file:
            meta_inf = zip_file.read("META-INF/container.xml")
            opf_path = self.get_opf_path(meta_inf)
            if opf_path is None:
                return None
            opf_root = ET.fromstring(zip_file.read(opf_path))

            cover_bytes = self.get_epub_cover(zip_file, opf_root, opf_path)

        return cover_bytes

    def get_cover_href (self, opf_root):
        meta_content = None
        all_metas = opf_root.findall(f".//{OPF_NS}meta")
        for meta in all_metas:
            meta_name = meta.get("name")
            if meta_name == "cover":
                meta_content = meta.get("content")
                if meta_content is None:
                    return None

        cover_href = None
        manifest = opf_root.find(f".//{OPF_NS}manifest")
        if manifest is None:
            return None

        for item in manifest.iter():
            if item.get("id") == meta_content:
                cover_href = item.get("href")
                break

        return cover_href

    def get_epub_cover(self, zip_file, opf_root, opf_path):
        cover_href = self.get_cover_href(opf_root)
        if cover_href is None:
            return None
        opf_dir = PurePosixPath(opf_path).parent
        cover_path = opf_dir / cover_href

        cover_binary = zip_file.read(str(cover_path))

        return cover_binary

    def get_opf_path(self, meta_inf):
        root = ET.fromstring(meta_inf)
        rootfile = root.find(f".//{CONTAINER_NS}rootfile")
        if rootfile is None:
            return None
        opf_path = rootfile.get("full-path")

        return opf_path

    def extract_epub_metadata(self, zip_file, opf_path):
        opf_info = zip_file.read(opf_path)
        opf_root = ET.fromstring(opf_info)

        metadata = {
            "title": self.get_title(opf_root),
            "author": self.get_author(opf_root),
            "genres": self.get_genres(opf_root),
            "publication_year": self.get_publish_year(opf_root),
            "publisher": self.get_publisher_info(opf_root),
            "isbn": self.get_isbn(opf_root),
            "language": self.get_language(opf_root),
            "annotation": self.get_annotation(opf_root),
            "cover": None,
        }

        return metadata

    def get_title (self, opf_root):
        title = opf_root.find(f".//{Dublin_Core_NS}title")
        if title is None:
            return None
        return title.text

    def get_author(self, opf_root):
        creator = opf_root.find(f".//{Dublin_Core_NS}creator")
        if creator is None:
            return None
        return creator.text

    def get_language (self, opf_root):
        language = opf_root.find(f".//{Dublin_Core_NS}language")
        if language is None:
            return None
        return language.text

    def get_publisher_info (self, opf_root):
        publisher = opf_root.find(f".//{Dublin_Core_NS}publisher")
        if publisher is None:
            return None
        return publisher.text

    def get_publish_year (self, opf_root):
        date = (opf_root.find(f".//{Dublin_Core_NS}date"))
        if date is None:
            return None
        date = int(date.text[:4])
        return date

    def get_genres (self, opf_root):
        subjects = opf_root.findall(f".//{Dublin_Core_NS}subject")
        return [subject.text.lower() for subject in subjects if subject.text]

    def get_annotation(self, opf_root):
        annotation = opf_root.find(f".//{Dublin_Core_NS}description")
        if annotation is None:
            return None
        return annotation.text

    def get_isbn(self, opf_root):
        identifiers = opf_root.findall(f".//{Dublin_Core_NS}identifier")
        isbn = ""
        for identifier in identifiers:
            scheme = identifier.get(f"{OPF_NS}scheme")
            identifire = identifier.text
            identifire = self.normalize_isbn(identifire)
            if self.is_valid_isbn(identifire):
                if len(isbn) < len(identifire):
                    isbn = identifire
        if isbn == "":
            isbn = None

        return isbn

class Fb2MetadataParser(MetadataParser):
    def parse(self, file_path):
        root = self.read_fb2(file_path)
        if root is None:
            return None
        return self.extract_fb2_metadata(root)

    def read_fb2(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except (ET.ParseError, FileNotFoundError):
            return None
        return root

    def get_description(self, root):
        description = root.find(f"{FB2_NS}description")

        if description is None:
            return None
        return description

    def extract_fb2_metadata(self, root):
        description = self.get_description(root)

        if description is None:
            return None

        title_info = self.get_title_info(description)
        publish_info = self.get_publish_info(description)

        metadata = {
            "title": self.get_title(title_info),
            "author": self.get_author(title_info),
            "genres": self.get_genres(title_info),
            "publication_year": self.get_publish_year(publish_info),
            "isbn": self.get_isbn(publish_info),
            "language": self.get_language(title_info),
            "annotation": self.get_annotation_text(self.get_annotation(title_info), ),
            "cover": None
        }

        return metadata

    def get_title_info(self, description):
        title_info = description.find(f"{FB2_NS}title-info")

        return title_info

    def get_title(self, title_info):
        if title_info is None:
            return None

        book_title = title_info.find(f"{FB2_NS}book-title")

        if book_title is None:
            return None

        return book_title.text

    def get_author(self, title_info):
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

    def get_genres(self, title_info):
        if title_info is None:
            return []

        genres = title_info.findall(f"{FB2_NS}genre")

        return [
            genre.text.lower()
            for genre in genres
            if genre.text
        ]

    def get_date(self, title_info):
        if title_info is None:
            return None

        date = title_info.find(f"{FB2_NS}date")
        if date is None:
            return None

        return date.text

    def get_publish_info(self, description):
        return description.find(f"{FB2_NS}publish-info")

    def get_publish_year(self, publish_info):
        if publish_info is None:
            return None

        year = publish_info.find(f"{FB2_NS}year")

        if year is None:
            return None

        return int(year.text)

    def get_isbn(self, publish_info):
        if publish_info is None:
            return None

        isbn = publish_info.find(f"{FB2_NS}isbn")

        if isbn is None:
            return None

        isbn = isbn.text

        isbn = self.normalize_isbn(isbn)

        if not self.is_valid_isbn(isbn):
            isbn = None
            return isbn

        return isbn

    def get_language(self, title_info):
        if title_info is None:
            return None

        language = title_info.find(f"{FB2_NS}lang")

        if language is None:
            return None

        return language.text

    def get_annotation(self, title_info):
        if title_info is None:
            return None

        annotation = title_info.find(f"{FB2_NS}annotation")

        if annotation is None:
            return None

        return annotation

    def get_annotation_text(self, annotation):
        if annotation is None:
            return None

        paragraphs = []

        for paragraph in annotation:
            if paragraph.text:
                text = "".join(paragraph.itertext()).strip()

                if text:
                    paragraphs.append(text)

        return "\n".join(paragraphs)

    def get_cover(self, file_path):
        root = self.read_fb2(file_path)

        if root is None:
            return None

        return self.get_cover_from_root(root)

    def get_cover_from_root(self, root):
        coverpage = root.find(f".//{FB2_NS}coverpage")

        if coverpage is None:
            return None

        image = coverpage.find(f"{FB2_NS}image")

        if image is None:
            return None

        href = image.get("{http://www.w3.org/1999/xlink}href")

        if not href:
            return None

        cover_id = href.lstrip("#")

        binary = root.find(
            f".//{FB2_NS}binary[@id='{cover_id}']"
        )

        if binary is None or not binary.text:
            return None

        try:
            return base64.b64decode(binary.text)
        except (ValueError, base64.binascii.Error):
            return None


if __name__ == "__main__":
    parser = EpubMetadataParser()
    metadata = parser.parse("d:\\_BOOKS\\_BOOKS_TEST\\A Merry Match.epub")

    parser_fb = Fb2MetadataParser()

    cover = parser.get_cover("d:\\_BOOKS\\_BOOKS_TEST\\A Merry Match.epub")
    print("EPUB = ",type(cover), "==", len(cover))

    cover_fb2 = parser_fb.get_cover("d:\\_BOOKS\\_BOOKS_TEST\\#Fantasy\Васильев Андрей. Файролл. Рассказы.fb2")
    print("FB2 = ",type(cover_fb2), "==", len(cover_fb2))

    #print(type(metadata["cover"]))
    #print(len(metadata["cover"]))




