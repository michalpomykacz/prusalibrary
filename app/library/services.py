from datetime import datetime

from django.db import transaction

from app.library.models import Book, Borrowing


@transaction.atomic
def borrow_book(book: Book, borrow_dt: datetime):
    book.borrowing_set.create(borrow_dt=borrow_dt)
    book.is_available = False
    book.borrowing_count += 1
    book.save()


@transaction.atomic
def return_book(book: Book, return_dt: datetime):
    book.borrowing_set.filter(return_dt__isnull=True).update(return_dt=return_dt)
    book.avg_borrowing_time = Borrowing.objects.book_avg_borrowing_time(book.id)
    book.is_available = True
    book.save()
