


def compare_metadata(book, metadata):
    differences = {}

    for key, new_value in metadata.items():
        if key == "source_path":
            continue

        old_value = getattr(book, key)

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
            setattr(book, field, data["new"])
        else:
            conflict_fields.append(field)
    return book, conflict_fields

def resolve_conflicts(book, differences, decisions):
    for field, data in differences.items():
        if data["empty"]:
            continue
        decision = decisions.get(field)

        if decision == "replace":
            setattr(book, field, data["new"])

        elif decision == "keep":
            continue
        elif decision == "add" and field == "genres":
            genres = add_unique_values(book.genres, data["new"])
            setattr(book, field, genres)

        elif decision == "add" and field == "annotation":
            annotation = book.annotation + "\n\n" + data["new"]
            setattr(book, field, annotation)

    return book

def add_unique_values(old_values, new_values):
    for value in new_values:
        if value not in old_values:
            old_values.append(value)

    return old_values

