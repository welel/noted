from celery import shared_task

from django.core.management import call_command


@shared_task
def telegram_report_task():
    call_command("telegram_report")
