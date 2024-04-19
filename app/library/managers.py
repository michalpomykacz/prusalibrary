from django.db import models


class BorrowingManager(models.Manager):

    def filter_book(self, book_id: int):
        return self.get_queryset().filter(book_id=book_id)

    def book_avg_borrowing_time(self, book_id: int) -> int:
        """Return the average borrowing time for a book in seconds."""
        result = (
            self.filter_book(book_id)
            .values("book_id")
            .annotate(
                avg_borrowing_time=models.Avg(
                    models.F("return_dt") - models.F("borrow_dt")
                )
            )
        )
        return result[0]["avg_borrowing_time"].days if result else 0

    def is_book_borrowed(self, book_id: int) -> bool:
        return self.filter_book(book_id).filter(return_dt__isnull=True).exists()
