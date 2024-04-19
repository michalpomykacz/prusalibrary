import pathlib
import csv

from django.core.management.base import BaseCommand

from app.library.models import Book, Author


class Command(BaseCommand):
    help = "Load library data from given CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        with pathlib.Path.open(options["csv_path"], "r") as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=1):
                author_names = row["authors"].split(",")

                book, _ = Book.objects.get_or_create(isbn=row["isbn"])
                book.title = row["title"]
                book.language_code = row["language_code"]
                book.original_publication_year = (
                    row["original_publication_year"] or None
                )
                book.save()

                for author_name in author_names:
                    author, _ = Author.objects.get_or_create(name=author_name)
                    book.authors.add(author)

        self.stdout.write(
            self.style.SUCCESS(f"Library data successfully loaded. Items: {i}")
        )
