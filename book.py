


class Book:
    def __init__(self, book_record):
        self.book_id = book_record.get('book_id')
        self.author = book_record.get('author')
        self.title = book_record.get('title')
        self.isbn = book_record.get('isbn')
        self.publisher = book_record.get('publisher')
        self.publication_year = book_record.get('publication_year')
        self.first_publication_year = book_record.get('first_publication_year')
        self.genres = book_record.get('genres')
        self.annotation =book_record.get('annotation')
        self.language = book_record.get('language')
        self.cover = book_record.get('cover')
        self.source_path = book_record.get('source_path')
        self.format = book_record.get('format')
        self.status = book_record.get('status')


