from models import Quote, Author
import sys

def search_quotes():
    while True:
        command = input("Enter command: ")
        if command.startswith("name:"):
            name = command.split("name:")[1].strip()
            author = Author.objects(fullname=name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
            else:
                print(f"No quotes found for author: {name}")
        elif command.startswith("tag:"):
            tag = command.split("tag:")[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith("tags:"):
            tags = command.split("tags:")[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)
        elif command == "exit":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    search_quotes()
