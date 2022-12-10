"""The module provides functions for transfering Markdown to HTML.
**Functions**
    markdown_to_html: transfers Markdown text into HTML via GitHub API.
    pick_markdown_to_html: transfer Markdown text into HTML (2 methods).
"""

import traceback
from typing import Tuple
import requests

from markdown2 import markdown


API_URL = "https://api.github.com/markdown/raw"
HEADERS = {"Content-Type": "text/plain"}


def markdown_to_html(text: str) -> Tuple[str, bool]:
    """Transfer Markdown text into HTML via GitHub API.

    API docs: https://docs.github.com/en/rest/reference/markdown
    Makes POST request to GitHub API for HTML code.
    Sends Markdown text in body of POST request to GitHub API.
    Gets HTML code of Markdown text and returns it with a flag.

    Args:
        text: the Markdown text to render in HTML.
    Returns:
        str: the HTML code or `text` if request is failed.
        bool: a success flag.
    """
    text_encoded = text.encode("utf-8", "ignore")

    if not isinstance(text_encoded, bytes):
        return text, False

    try:
        response = requests.post(
            API_URL, data=text_encoded, headers=HEADERS, timeout=10
        )
        if response.status_code == 200:
            return response.text, True
    except requests.exceptions.ConnectionError as erorr:
        # TODO: Log this
        print(
            "Markdown API request is failed:\n",
            traceback.print_tb(erorr.__traceback__),
        )

    return text, False


def pick_markdown_to_html(text: str) -> str:
    """Transfer Markdown text into HTML.

    The function transfers Markdown text into HTML using 2 independent
    methods. First method via GitHub API, if it fails, the function uses
    `markdown2` module. And returns first success result.

    Args:
        text: the Markdown text to render in HTML.
    Returns:
        The rendered HTML code.
    """
    html, success = markdown_to_html(text)
    if success:
        return html
    return markdown(text=text)
