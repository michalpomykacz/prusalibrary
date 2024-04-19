from django.urls import path

from app.library.api_views import BookList, BookDetail, BookBorrowing, BookReturn

app_name = "library"

urlpatterns = [
    path("books", BookList.as_view(), name="books"),
    path("books/<int:pk>", BookDetail.as_view(), name="book"),
    path("books/borrow", BookBorrowing.as_view(), name="book_borrowing"),
    path("books/return", BookReturn.as_view(), name="book_return"),
]
