import json
from models import Author, Quote

# Завантаження даних авторів
with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)
    for author in authors_data:
        a = Author(**author)
        a.save()

# Завантаження цитат
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)
    for quote in quotes_data:
        author = Author.objects(fullname=quote['author']).first()
        if author:
            q = Quote(tags=quote['tags'], author=author, quote=quote['quote'])
            q.save()