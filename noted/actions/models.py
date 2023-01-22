import datetime

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from actions.base import NEW, CREATE, FOLLOW, DOWNLOAD, BOOKMARK, LIKE
from actions.notifications import create_notification


class ActionManager(models.Manager):
    def create_action(
        self, actor, verb: str, target=None, notify: bool = False
    ) -> bool:
        """A create instance shortcut function for :model:`Action`.
        Doesn't create similar actions within a minute.

        Args:
            actor: initiactor .
            verb: describing the action.
            target: any model instance to which the action is directed.
            notify: if true creates `Notification` of the action.
        Returns:
            A boolean code - is an actions was created.
        """
        if settings.TEST_MODE:
            return False
        # check for any similar action made in the last minutes
        last_minute = timezone.now() - datetime.timedelta(seconds=60)
        actor_ct = ContentType.objects.get_for_model(actor)
        similar_actions = self.filter(
            verb=verb,
            created__gte=last_minute,
            actor_ct=actor_ct,
            actor_id=actor.id,
        )
        if target:
            target_ct = ContentType.objects.get_for_model(target)
            similar_actions = similar_actions.filter(
                target_ct=target_ct, target_id=target.id
            )
        if not similar_actions:
            action = Action(actor=actor, verb=verb, target=target)
            action.save()
            if notify:
                create_notification(actor, verb, target)
            return True
        return False


class Action(models.Model):
    """Store users actions on the site.

    **Fields**
        actor: an object that initiacte an action.
        actor_ct: a content type of the actor.
        actor_id: an object id of the actor.
        verb: an action name.
        created: datetime of an action.
        target_ct: an object model on which an action is directed.
        target_id: an object id on which an action is directed.
        target: an object on which an action is directed.

    """

    ACTIONS = [
        (NEW, _(NEW)),
        (CREATE, _(CREATE)),
        (FOLLOW, _(FOLLOW)),
        (BOOKMARK, _(BOOKMARK)),
        (LIKE, _(LIKE)),
        (DOWNLOAD, _(DOWNLOAD)),
    ]

    actor_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="actor_obj",
        on_delete=models.CASCADE,
    )
    actor_id = models.PositiveIntegerField(
        null=True, blank=True, db_index=True
    )
    actor = GenericForeignKey("actor_ct", "actor_id")
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