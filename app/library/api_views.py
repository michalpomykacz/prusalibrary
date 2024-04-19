from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from app.library.filters import BookFilter
from app.library.models import Book
from app.library.serializers import (
    BookSerializer,
    BookBorrowingSerializer,
    BookReturnSerializer,
)
from app.library.services import borrow_book, return_book


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = BookFilter


class BookDetail(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookBorrowing(APIView):

    def post(self, request, *args, **kwargs):
        serializer = BookBorrowingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrow_book(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class BookReturn(APIView):

    def post(self, request, *args, **kwargs):
        serializer = BookReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return_book(**serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
