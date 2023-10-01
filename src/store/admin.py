from django.contrib import admin

from store.models import Product, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('model', 'version', 'quantity')
    # readonly_fields = ('model', 'version', 'serial', 'created',)


@admin.register(Product)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('robot', 'price', 'display_quantity')

    # readonly_fields = ('model', 'version', 'serial', 'created',)

    def display_quantity(self, obj):
        return obj.robot.quantity

    display_quantity.short_description = 'Остаток'
