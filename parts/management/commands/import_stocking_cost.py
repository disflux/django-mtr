from django.core.management.base import BaseCommand, CommandError
from inventory.models import PartValuation
from parts.models import Part
import csv

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('scost.csv', 'rb') as csvfile:
            invreader = csv.reader(csvfile, delimiter=',')
            not_found = []
            sum = 0
            PartValuation.objects.all().delete()
            for row in invreader:
                part_number = row[0].strip().upper()
                uom = row[1].strip().upper()
                applied = row[2].replace(",","")
                on_hand = row[3].replace(",","")
                stocking_cost = row[4].strip().replace(",","")
                #self.stdout.write("PART: %s | QTY: %s | COST: %s" % (part_number, on_hand, stocking_cost))

                try:
                    part = Part.objects.get(part_number=part_number)
                    v, created = PartValuation.objects.get_or_create(part=part)
                    v.uom = uom
                    v.quantity = on_hand
                    v.stocking_cost = stocking_cost
                    v.ext_value = float(v.stocking_cost) * float(v.quantity)
                    v.applied_quantity = applied
                    self.stdout.write("PART: %s | QTY: %s | COST: %s | EXT: %s" % (v.part.part_number, v.quantity, v.stocking_cost, v.ext_value))
                    v.save()
                    sum += v.ext_value
                except:
                    not_found.append(part_number)

            self.stdout.write("\n\nPARTS NOT FOUND: ")
            print not_found
            self.stdout.write("\n\nValuation: %s" % sum)

        self.stdout.write("\nFinished.\n")
