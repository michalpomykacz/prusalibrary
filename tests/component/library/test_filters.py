from typing import Any

import pytest

from app.library.models import Book
from app.library.filters import BookFilter


@pytest.mark.component
@pytest.mark.django_db()
class TestBookFilter:

    @pytest.mark.parametrize(
        "filters, expected_isbns",
        [
            pytest.param({"isbn": "439023483"}, ["439023483"], id="isbn filter"),
            pytest.param({"title": "Hunger"}, ["439023483"], id="title search"),
            pytest.param(
                {"original_publication_year__gt": 2000},
                ["439023483"],
                id="publication_year gt filter",
            ),
            pytest.param(
                {"original_publication_year__lt": 2000},
                ["439554934"],
                id="publication_year lt filter",
            ),
            pytest.param(
                {"original_publication_year": 1997},
                ["439554934"],
                id="publication_year exact filter",
            ),
            # TODO add more test cases for other field filters
        ],
    )
    def test_filter_books(
        self,
        books_in_db: list[Book],
        filters: dict[str, Any],
        expected_isbns: list[str],
    ):
        # TODO use a fixture with more items in db
        queryset = Book.objects.all()
        book_filter = BookFilter(filters, queryset=queryset)

        assert [book.isbn for book in book_filter.qs] == expected_isbns
