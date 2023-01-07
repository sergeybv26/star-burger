from django.contrib import admin

from addressapp.models import AddressCoordinate


@admin.register(AddressCoordinate)
class AddressCoordinateAdmin(admin.ModelAdmin):
    list_display = ['address']
