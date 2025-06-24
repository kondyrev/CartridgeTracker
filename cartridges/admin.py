from django.contrib import admin
from .models import Department, Printer, Cartridge, UsageRecord, PrinterCartridge, CartridgeInventory

admin.site.register(Department)
admin.site.register(Printer)
admin.site.register(Cartridge)
admin.site.register(UsageRecord)
admin.site.register(PrinterCartridge)
admin.site.register(CartridgeInventory)