from book_catalog import BookCatalog
from process_manager import ProcessManager
from database import open_database, book_data_to_objects
from main_gui import run_app


if __name__ == "__main__":
    book_data = open_database()
    book_objects = book_data_to_objects(book_data)
    book_catalog = BookCatalog(book_objects)
    process_manager = ProcessManager(book_catalog)

    run_app(book_catalog, process_manager)