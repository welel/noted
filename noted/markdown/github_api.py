import requests
import traceback


URL = 'https://api.github.com/markdown/raw'
HEADERS = {'Content-Type': 'text/plain'}


def get_markdown_html(raw_markdown) -> (str, bool):
    """Makes POST request to GitHub API for html code.

    API docs: https://docs.github.com/en/rest/reference/markdown
    Sends `body_raw` in body of POST request to GitHub API.
    Gets html code of markdown text and returns it.

    Returns:
        str: html code or raw_markdown (if request is failed).
        bool: a success flag.

    """
    raw_markdown_encoded = raw_markdown.encode('utf-8', 'ignore')

    if not isinstance(raw_markdown_encoded, bytes):
        return raw_markdown, False

    try:
        response = requests.post(
            URL, data=raw_markdown_encoded, headers=HEADERS
        )
        if response.status_code == 200:
            return response.text, True
    except requests.exceptions.ConnectionError as e:
        # TODO: Log this
        print('Markdown API request is failed:',
              traceback.print_tb(e.__traceback__))

    return raw_markdown, False
