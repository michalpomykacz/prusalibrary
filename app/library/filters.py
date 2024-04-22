from django_filters import FilterSet, CharFilter

from app.library.models import Book


class BookFilter(FilterSet):

    title = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Book
        fields = {
            "isbn": ["exact"],
            "language_code": ["exact"],
            "is_available": ["exact"],
            "original_publication_year": ["exact", "gte", "lte"],
            "avg_borrowing_time": ["exact", "gte", "lte"],
            "borrowing_count": ["exact", "gte", "lte"],
        }
