from django.core.management.base import BaseCommand, CommandError
from reports.models import Report
import gc

class Command(BaseCommand):
    def handle(self, *args, **options):
        reports = Report.objects.all()
        for r in reports:
            r.lot_number = r.id + 10000
            r.save()

        self.stdout.write("\nFinished.\n")
