from django.db import models

from app.library.managers import BorrowingManager


class Author(models.Model):

    name = models.CharField(max_length=100)


class Book(models.Model):

    isbn = models.CharField(max_length=13, unique=True)
    title = models.TextField()
    language_code = models.CharField(max_length=35, db_index=True, null=True)
    original_publication_year = models.SmallIntegerField(db_index=True, null=True)
    avg_borrowing_time = models.PositiveIntegerField(
        db_index=True, help_text="In days", default=0
    )
    borrowing_count = models.PositiveIntegerField(default=0, db_index=True)
    is_available = models.BooleanField(default=True, db_index=True)
    authors = models.ManyToManyField(Author)


class Borrowing(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_dt = models.DateTimeField()
    return_dt = models.DateTimeField(null=True)

    objects = BorrowingManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(  # This index is implemented to prevent the same book from being borrowed more than once at a time.
                fields=["book"],
                name="currently_borrowed_book",
                condition=models.Q(return_dt__isnull=True),
            ),
            models.CheckConstraint(
                check=models.Q(return_dt__gte=models.F("borrow_dt")),
                name="return_dt_gte_borrow_dt",
            ),
        ]
