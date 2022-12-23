from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Make migrations and migrate all apps."

    def handle(self, *args, **options):
        call_command("makemigrations", "tags")
        call_command("makemigrations", "users")
        call_command("makemigrations", "content")
        call_command("migrate")
