from metadata import Fb2MetadataParser, EpubMetadataParser


class ParserFactory:
    @staticmethod
    def create_parser(book_format):
        if book_format == "fb2":
            parser = Fb2MetadataParser()
        elif book_format == "epub":
            parser = EpubMetadataParser()
        # elif book_format == "pdf":
        #     pass
        # elif book_format == "mobi":
        #     pass
        # elif book_format == "txt":
        #     pass
        # elif book_format == "djvu":
        #     pass
        else:
            return None

        return parser


