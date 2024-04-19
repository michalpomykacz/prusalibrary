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
            "original_publication_year": ["exact", "gt", "lt"],
            "avg_borrowing_time": ["exact", "gt", "lt"],
            "borrowing_count": ["exact", "gt", "lt"],
        }
