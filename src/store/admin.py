from django.contrib import admin

from store.models import Warehouse, Product


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('model', 'version', 'quantity')
    # readonly_fields = ('model', 'version', 'serial', 'created',)


@admin.register(Product)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('robot', 'price')
    # readonly_fields = ('model', 'version', 'serial', 'created',)
