from xml.etree.ElementTree import VERSION

DEBUG = True

TEST_BOOKS = {
  "last_updated": "2026-08-05",
  "book_count": 7,
  "books": [
    {
      "id": 1,
      "title": "Война и мир",
      "author": "Лев Толстой",
      "year": 1869,
      "genre": ["Роман"],
      "path": "Русская классика",
      "format": "fb2"
    },
    {
      "id": 2,
      "title": "1984",
      "author": "Джордж Оруэлл",
      "year": 1949,
      "genre": ["Антиутопия"],
      "path": "Зарубежная классика",
      "format": "fb2"
    },
    {
      "id": 3,
      "title": "Пикник на обочине",
      "author": "Братья Стругацкие",
      "year": 1972,
      "genre": ["Научная фантастика"],
      "path": "Советская фантастика",
      "format": "fb2"
    },
    {
      "id": 4,
      "title": "Мастер и Маргарита",
      "author": "Михаил Булгаков",
      "year": 1967,
      "genre": ["Роман"],
      "path": "Русская классика",
      "format": "fb2"
    },
    {
      "id": 5,
      "title": "Чистый код",
      "author": "Роберт Мартин",
      "year": 2008,
      "genre": ["Программирование"],
      "path": "Техническая литература",
      "format": "fb2"
    },
    {
      "id": 6,
      "title": "Затерянный мир",
      "author": "Артур Конан Дойл",
      "year": 1912,
      "genre": ["Приключения"],
      "path": "Зарубежная классика",
      "format": "fb2"
    },
    {
      "id": 7,
      "title": "Дивный новый мир",
      "author": "Олдос Хаксли",
      "year": 1932,
      "genre": ["Антиутопия"],
      "path": "Зарубежная классика",
      "format": "fb2"
    }
  ]
}

VERSION = "0.0.5"