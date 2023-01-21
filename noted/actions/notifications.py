from typing import Union, List

from notifications.signals import notify

from django.utils.functional import SimpleLazyObject

from actions.base import CREATE, FOLLOW, LIKE
from content.models import Note
from tags.models import get_tag_followers, UnicodeTag
from users.models import User, Following


RECIPIENTS_GETTERS = {
    (User, FOLLOW, User): lambda _, followed_user: followed_user,
    (User, LIKE, Note): lambda _, note: note.author,
    # TODO: Exclude AUTHOR of Tag
    (UnicodeTag, CREATE, Note): lambda tag, note: get_tag_followers(tag),
    (User, CREATE, Note): lambda author, _: Following.objects.get_follower(
        author
    ),
}


def get_recipients(actor, verb: str, target) -> Union[User, List[User], None]:
    actor_type = User if isinstance(actor, SimpleLazyObject) else type(actor)
    targ_type = User if isinstance(target, SimpleLazyObject) else type(target)
    recipient_function = RECIPIENTS_GETTERS[(actor_type, verb, targ_type)]
    return recipient_function(actor, target)


def create_notification(actor, verb: str, target):
    notify.send(
        actor,
        verb=verb,
        recipient=get_recipients(actor, verb, target),
        target=target,
    )
