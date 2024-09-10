from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.management import BaseCommand
from mailing.services import start_scheduler, scheduler


class Command(BaseCommand):

    def handle(self, *args, **options):
        if scheduler.running:
            scheduler.shutdown()
        start_scheduler()