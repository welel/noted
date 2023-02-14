from datetime import datetime, timedelta
import os
import requests
import logging

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from content.models import Note
from users.models import User


logger = logging.getLogger("emails")


class Command(BaseCommand):
    help = "Sends a report about new users and notes to Telegram Service Bot."

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
        if not (self.TELEGRAM_BOT_TOKEN and self.TELEGRAM_CHAT_ID):
            raise CommandError(
                "Specify TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to"
                " the environment."
            )

    def handle(self, *args, **options):
        last_day = timezone.now() - timedelta(days=1)
        last_day_start = datetime(
            last_day.year, last_day.month, last_day.day, tzinfo=last_day.tzinfo
        )

        new_users = self._get_users_report(date_joined__gt=last_day_start)
        new_notes = self._get_notes_report(created__gt=last_day_start)

        report = "<i>Report {}</i>\n\n{}{}".format(
            last_day.strftime("%m/%d/%Y"),
            new_users + "\n\n" if new_users else "No new users.\n\n",
            new_notes + "\n\n" if new_notes else "No new notes.\n\n",
        )

        url = f"https://api.telegram.org/{self.TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": self.TELEGRAM_CHAT_ID,
            "parse_mode": "HTML",
            "text": report,
        }
        response = requests.get(url, data=data)
        if response.status_code != 200:
            logger.error(response.json())
            raise CommandError(
                "Request is failed: status code " + str(response.status_code)
            )

    def _get_users_report(self, **kwargs) -> str:
        new_users = User.objects.filter(**kwargs)
        if not new_users:
            return ""

        report = "<b>New users</b>:\n{}"
        return report.format(
            "\n".join(
                [
                    f"<code>{user.username}</code> - {user.date_joined.strftime('%H:%M')}"
                    for user in new_users
                ]
            )
        )

    def _get_notes_report(self, **kwargs) -> str:
        new_notes = Note.objects.filter(**kwargs)
        if not new_notes:
            return ""

        report = "<b>New notes:</b>\n{}"
        return report.format(
            "\n".join(
                [
                    "<code>{}</code>: {}".format(
                        note.author if note.author else "Anon", note.title
                    )
                    for note in new_notes
                ]
            )
        )
