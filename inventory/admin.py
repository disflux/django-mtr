from django.contrib import admin
from inventory.models import InventoryLocation, InventoryCount, PartValuation, InventoryValuation

admin.site.register(InventoryLocation)
admin.site.register(InventoryCount)
admin.site.register(PartValuation)
admin.site.register(InventoryValuation)


