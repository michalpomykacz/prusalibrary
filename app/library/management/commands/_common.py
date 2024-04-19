import abc
import datetime

from django.core.management.base import BaseCommand
import requests


class BaseBookOperationCommand(BaseCommand, abc.ABC):

    @property
    @abc.abstractmethod
    def operation_name(self) -> str:
        """Provide book operation name."""

    @abc.abstractmethod
    def _call_api(
        self, host: str, book_id: str, dt: datetime.datetime
    ) -> requests.Response:
        """Call API for book operation."""

    def add_arguments(self, parser):
        parser.add_argument("host", type=str)
        parser.add_argument("book_id", type=str)
        parser.add_argument(
            "dt", type=str, help="Datetime in format YYYY-MM-DD HH:MM:SS"
        )

    def handle(self, *args, **options):
        response = self._call_api(
            options["host"],
            options["book_id"],
            datetime.datetime.strptime(options["dt"], "%Y-%m-%d %H:%M:%S"),
        )
        if not response.ok:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to {self.operation_name} book. Error: {response.text}"
                )
            )
            return
        self.stdout.write(self.style.SUCCESS(f"Book {self.operation_name} successful."))
