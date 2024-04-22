from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from app.library.exceptions import LibraryError


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        match exc:
            case LibraryError():
                response = Response(data=exc.detail, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return response
