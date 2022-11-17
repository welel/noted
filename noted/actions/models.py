from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from user.models import User


class Action(models.Model):
    """Store users actions on the site.

    **Fields**
        user: a user that do an aciton.
        verb: an action name.
        created: datetime of an action.
        target_ct: an object model on which an action is directed.
        target_id: an object id on which an action is directed.
        target: an object on which an action is directed.
    
    """
    NEW_NOTE = 'new_note'
    NEW_COMMENT = 'new_comment'
    NEW_USER = 'new_user'
    FOLLOW = 'follow'
    BOOKMARK = 'bookmark'
    LIKE = 'like'
    ACTIONS = [
        (NEW_NOTE, 'A user posted a note.'),
        (NEW_COMMENT, 'A user left a comment to a note.'),
        (NEW_USER, 'Has created an account.'),
        (FOLLOW, 'A user stared following another user.'),
        (BOOKMARK, 'A user added a note to his bookmarks.'),
        (LIKE, 'A user liked a note.'),
    ]

    user = models.ForeignKey(User, related_name='actinos', db_index=True,
        on_delete=models.CASCADE)
    verb = models.CharField(max_length=255, choices=ACTIONS)
    created = models.DateField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True,
        related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True,
        db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)
