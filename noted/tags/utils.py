from typing import List

from common.logging import logit


@logit
def custom_tag_string(tag_string: str) -> List[str]:
    """Parses tag string to list of tags.

    Args:
        tag_string: A string of tags separated by commas or spaces.

    Returns:
        A list of tags.
    """
    if not tag_string:
        return []
    if "," not in tag_string and " " not in tag_string:
        return [tag_string]
    tags = []
    for tag in tag_string.split(","):
        tags.append(tag.strip().lower().replace(" ", "-"))
    return tags
