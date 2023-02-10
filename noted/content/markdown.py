"""The module provides functions for transfering Markdown to HTML.

**Functions**
    check_remainig_api_ratelimit: log how many API requests left.
    markdown_to_html: transfers Markdown text into HTML via GitHub API.
    pick_markdown_to_html: transfer Markdown text into HTML (2 methods).
"""

import logging
import traceback
from typing import Tuple

import requests
from markdown2 import markdown

from django.conf import settings


logger = logging.getLogger("markdown")

API_URL = "https://api.github.com/markdown/raw"
HEADERS = {
    "Content-Type": "text/plain",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def check_remainig_api_ratelimit(response):
    """Check GitHub API response on remaning requests and log it."""
    try:
        limit = int(response.headers.get("X-RateLimit-Limit"))
        remaining = int(response.headers.get("X-RateLimit-Remaining"))
    except ValueError:
        logger.warning("Bad ratelimit headers.")
    if remaining < 20:
        logger.warning("Left less that 20 requests: " + str(remaining))
    logger.info(f"Limit: {limit} | Left: {remaining}")


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
            check_remainig_api_ratelimit(response)
            return response.text, True
    except requests.exceptions.ConnectionError as erorr:
        logger.error(
            "Markdown API request is failed:\n" + traceback.format_exc()
        )
    logger.warning(
        "Markdown API request is failed:\nStatus code: {code}\nHEADERS: \
            {headers}\nJSON: {json}\nRAW: {raw}\nTEXT: {text}\n".format(
            code=response.status_code,
            headers=response.headers,
            json=response.json,
            raw=response.raw,
            text=response.text,
        )
    )
    return text, False


def pick_markdown_to_html(text: str) -> str:
    """Transfer Markdown text into HTML.

    The function transfers Markdown text into HTML using 2 independent
    methods. First method via GitHub API, if it fails, the function uses
    `markdown2` module. And returns first success result.

    Args:
        text: The Markdown text to render in HTML.

    Returns:
        The rendered HTML code.
    """
    if not settings.TEST_MODE:
        html, success = markdown_to_html(text)
        if success:
            return html
    return markdown(text=text)
