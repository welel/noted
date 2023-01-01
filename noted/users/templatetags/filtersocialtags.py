from django import template


register = template.Library()


@register.filter
def twitter_url(username: str) -> str:
    return "https://twitter.com/{}/".format(username)


@register.filter
def facebook_url(username: str) -> str:
    return "https://facebook.com/{}/".format(username)


@register.filter
def github_url(username: str) -> str:
    return "https://github.com/{}/".format(username)
