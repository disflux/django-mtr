from django.contrib import admin
from inventory.models import InventoryLocation, InventoryCount

admin.site.register(InventoryLocation)
admin.site.register(InventoryCount)

