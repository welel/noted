import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from actions.models import Action
from user.models import User

def create_action(user: User, verb: str, target=None) -> bool:
    """A create instance shortcut function for :model:`Action`.

    Doesn't create similar actions within a minute.
    
    Args:
        user: a user who is performing an aciton.
        verb: describing the action.
        target: any model instance to which the action is directed.

    Returns:
        A boolean code - is an actions was created. 
    """
    # check for any similar action made in the last minutes
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions= Action.objects.filter(user_id=user.id, verb=verb,
        created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions= similar_actions.filter(target_ct=target_ct,
            target_id=target.id)
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
