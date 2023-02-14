from typing import List


def custom_tag_string(tag_string: str) -> List[str]:
    """Parses string with tags to list of tags.

    Splits by commas and replaces spaces on dashes.

    Args:
        tag_string: A string of tags separated by commas.

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
