import datetime

import requests

from app.library.management.commands._common import BaseBookOperationCommand


class Command(BaseBookOperationCommand):
    help = "Return a book"
    operation_name = "return"

    def _call_api(
        self, host: str, book_id: str, dt: datetime.datetime
    ) -> requests.Response:
        return requests.post(
            f"{host}/api/v1/books/return",
            json={"book": book_id, "return_dt": dt.isoformat()},
        )
