from django.core.management.base import BaseCommand, CommandError
from reports.models import Report
from parts.models import Part
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('allinventory.csv', 'rb') as csvfile:
            invreader = csv.reader(csvfile, delimiter=',')
            i = 0
            for row in invreader:
                part_number = row[0].strip().upper()
                description = row[1].strip().upper().replace("''", '"')
                product_code = row[2].strip().upper()
                part, _created = Part.objects.get_or_create(part_number=part_number)
                if not part.description:
                    part.description = description
                part.product_code = product_code
                part.save()
                print "PART: %s | DESC: %s | P: %s" % (part_number, description, product_code)
                i += 1

        self.stdout.write("\nFinished.\n")
