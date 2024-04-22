

class LibraryError(Exception):
    """Base class for Library business logic exceptions."""

    def __init__(self, detail: str) -> None:
        self.detail = detail

    def __str__(self) -> str:  # noqa: D105
        return self.detail
