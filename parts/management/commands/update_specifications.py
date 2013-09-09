from django.core.management.base import BaseCommand, CommandError
from reports.models import Report
from parts.models import Part

class Command(BaseCommand):
    def handle(self, *args, **options):
        reports = Report.objects.all()
        for r in reports:
            part = r.part_number
            self.stdout.write("Updating %s to %s" % (part, r.specification))
            part.specification = r.specification
            part.save()

        self.stdout.write("\nFinished.\n")
