import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.models import User


class ActionManager(models.Manager):
    def create_action(self, user: User, verb: str, target=None) -> bool:
        """A create instance shortcut function for :model:`Action`.
        Doesn't create similar actions within a minute.

        Args:
            user: a user who is performing an aciton.
            verb: describing the action.
            target: any model instance to which the action is directed.
        Returns:
            A boolean code - is an actions was created.
        """
        if settings.TEST_MODE:
            return False
        # check for any similar action made in the last minutes
        now = timezone.now()
        last_minute = now - datetime.timedelta(seconds=60)
        similar_actions = self.filter(
            user_id=user.id, verb=verb, created__gte=last_minute
        )
        if target:
            target_ct = ContentType.objects.get_for_model(target)
            similar_actions = similar_actions.filter(
                target_ct=target_ct, target_id=target.id
            )
        if not similar_actions:
            action = Action(user=user, verb=verb, target=target)
            action.save()
            return True
        return False


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

    NEW_NOTE = "new_note"
    NEW_SOURCE = "new_source"
    NEW_USER = "new_user"
    BOOKMARK = "bookmark"
    LIKE = "like"
    DOWNLOAD = "download"
    FOLLOW_TAG = "follow_tag"
    FOLLOW_USER = "follow_user"
    ACTIONS = [
        (NEW_NOTE, _("A user posted a note.")),
        (NEW_SOURCE, _("A user posted a note with new source.")),
        (NEW_USER, _("Has created an account.")),
        (FOLLOW_TAG, _("A user stared following a tag.")),
        (BOOKMARK, _("A user added a note to his bookmarks.")),
        (LIKE, _("A user liked a note.")),
        (DOWNLOAD, _("A user downloaded a note.")),
        (FOLLOW_USER, _("A user stared following another user.")),
    ]

    user = models.ForeignKey(
        User, related_name="actinos", db_index=True, on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255, choices=ACTIONS)
    created = models.DateField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )
    target = GenericForeignKey("target_ct", "target_id")
    objects = ActionManager()

    class Meta:
        ordering = ("-created",)
