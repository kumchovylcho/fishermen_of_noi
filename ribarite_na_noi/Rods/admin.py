from django.contrib import admin

from ribarite_na_noi.Rods.models import Rod


@admin.register(Rod)
class RodsAdmin(admin.ModelAdmin):
    list_display = ("rod_name", "rod_type", "length", "guides", "action", "created_by", "price")
    ordering = ("-price",)
    list_filter = ("rod_type", "length", "guides", "action")
