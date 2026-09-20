

def delete_books(book_data, id_number):
    for i, book in enumerate(book_data["books"]):
        if book["book_id"] == id_number:
            deleted_book = book_data["books"].pop(i)
            book_data["book_count"] = len(book_data["books"])
            break
    else:
        print(f"Книга с id {id_number} не найдена.")

def find_book(book_data, word):
    query_words = word.lower().split()
    found_books = []
    for book in book_data["books"]:
        book_lower = book["title"].lower()
        if all(word in book_lower for word in query_words):
            found_books.append(book)

    return found_books

def compare_metadata(book, metadata):
    differences = {}

    for key, new_value in metadata.items():
        if key == "path":
            continue

        old_value = book.get(key)

        if old_value != new_value:
            differences[key] = {
                "old": old_value,
                "new": new_value,
                "empty": is_empty_value(old_value)
            }

    return differences

def is_empty_value(value):
    return value is None or value == "" or value == []

def process_metadata_differences(differences, book):
    conflict_fields = []

    for field, data in differences.items():
        if data["empty"]:
            book[field] = data["new"]
        else:
            conflict_fields.append(field)
    return book, conflict_fields

def resolve_conflicts(book, differences, decisions):
    for field, data in differences.items():
        if data["empty"]:
            continue
        decision = decisions.get(field)


        if decision == "replace":
            book[field] = data["new"]

        elif decision == "keep":
            continue
        elif decision == "add" and field == "genres":
            book[field] = add_unique_values(book[field], data["new"])
        elif decision == "add" and field == "annotation":
            book[field] = book[field] + "\n\n" + data["new"]

    return book

def add_unique_values(old_values, new_values):
    for value in new_values:
        if value not in old_values:
            old_values.append(value)

    return old_values

