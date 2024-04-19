from rest_framework import serializers

from app.library.models import Book, Author, Borrowing


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("name",)


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "isbn",
            "title",
            "is_available",
            "original_publication_year",
            "avg_borrowing_time",
            "borrowing_count",
            "authors",
        )


class BookBorrowingSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    borrow_dt = serializers.DateTimeField()

    class Meta:
        model = Borrowing
        fields = [
            "book",
            "borrow_dt",
        ]

    def validate(self, data):
        data = super().validate(data)
        if not data["book"].is_available:
            raise serializers.ValidationError("Book is not available.")
        return data


class BookReturnSerializer(serializers.Serializer):

    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    return_dt = serializers.DateTimeField()

    class Meta:
        model = Borrowing
        fields = [
            "book",
            "return_dt",
        ]

    def validate(self, data):
        data = super().validate(data)
        if not Borrowing.objects.is_book_borrowed(data["book"].id):
            raise serializers.ValidationError("Book is not borrowed.")
        return data
