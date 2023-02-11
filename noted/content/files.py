from dataclasses import dataclass
from enum import Enum
from typing import Literal, TypedDict


# File extensions
MD: str = "md"
HTML: str = "html"
PDF: str = "pdf"

CONTENT_TYPE_MD = "text/markdown; charset=UTF-8"
CONTENT_TYPE_HTML = "text/html; charset=utf-8"
CONTENT_TYPE_PDF = "application/pdf"

CONTENT_TYPES = {
    MD: CONTENT_TYPE_MD,
    HTML: CONTENT_TYPE_HTML,
    PDF: CONTENT_TYPE_PDF,
}


class NoteFile(TypedDict):
    content: str
    name: str
    content_type: str


class BadNoteFileExtension(Exception):
    """Exception raised when passes a not supported file extension.

    Attributes:
        message: Explanation of the error.
    """

    def __init__(
        self,
        file_extention: str,
        message="Note file is not support the extention",
    ):
        self.message = message + " - " + file_extention
        super().__init__(self.message)
