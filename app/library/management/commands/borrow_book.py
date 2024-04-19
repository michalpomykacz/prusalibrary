import datetime

import requests

from app.library.management.commands._common import BaseBookOperationCommand


class Command(BaseBookOperationCommand):
    help = "Borrow a book"
    operation_name = "borrow"

    def _call_api(
        self, host: str, book_id: str, dt: datetime.datetime
    ) -> requests.Response:
        return requests.post(
            f"{host}/api/v1/books/borrow",
            json={"book": book_id, "borrow_dt": dt.isoformat()},
        )
