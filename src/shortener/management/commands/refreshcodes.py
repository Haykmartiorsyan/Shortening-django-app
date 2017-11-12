from django.core.management.base import BaseCommand, CommandError
from shortener.models import KirrUrl


class Command(BaseCommand):
    help = 'Refresh all KirrUrl shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('items', type=int)

    def handle(self, *args, **options):
        print(options)
        return KirrUrl.objects.refresh_shortcodes(items=options['items'])
