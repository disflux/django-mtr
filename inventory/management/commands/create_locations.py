from django.core.management.base import BaseCommand, CommandError
from inventory.models import InventoryLocation

class Command(BaseCommand):
    def handle(self, *args, **options):
        location_type = args[0]
        if location_type == 'rack':
            self.stdout.write("Creating Rack Locations")
            #rack_rows = ['A', 'B', 'C', 'H', 'I', 'J', 'K', 'L']
            rack_rows = ['CP']
            for row in rack_rows:
                for i in range(1,6):
                    for j in range(0,11):
                        location_code = "%s-%s%02d" % (row, i, j)
                        location, created = InventoryLocation.objects.get_or_create(location_code=location_code)
                        location.count_complete = False
                        location.save()
                        self.stdout.write("Added location %s" % (location_code, ))
        
        if location_type == 'sp':
            self.stdout.write("Creating SP Locations")
            prefix = 'SP'
            for i in range(1, 18):
                for j in range(0, 7):
                    location_code = "%s-%02d-%02d" % (prefix, i, j)
                    location, created = InventoryLocation.objects.get_or_create(location_code=location_code)
                    location.count_complete = False
                    location.save()
                    self.stdout.write("Added location %s" % (location_code, ))
                    

        
        if location_type == 'atr':
            self.stdout.write("Creating atr Locations")
            prefix = 'ATR'
            for i in range(1, 6):
                for j in range(1, 11):
                    location_code = "%s-%02d-%02d" % (prefix, i, j)
                    location, created = InventoryLocation.objects.get_or_create(location_code=location_code)
                    location.count_complete = False
                    location.save()
                    self.stdout.write("Added location %s" % (location_code, ))
                                   
        self.stdout.write("\nFinished.\n")