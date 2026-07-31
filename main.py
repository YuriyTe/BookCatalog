"""
BookCatalog
Главный файл программы
версия 0.0.1
"""

print("BookCatalog, версия 0.0.1")
print('Добро пожаловать!')

print('Add book to list. When you want to stop adding, just print "stop"')


book_list = []
while True:
    name = input('Введи название книги: ').strip()
    if name == 'stop':
        break
    elif name == '':
        print('Вы не ввели название книги')
    else:
        book_list.append(name)

print('='*30)
print(f'В библиотеке {len(book_list)} книг(и)')
print()

for number, book in enumerate(book_list, start=1):
    print(f'{number:2d}. {book}')

print('='*30)

