from django.contrib import admin

from ribarite_na_noi.Chepareta.models import Chepare


@admin.register(Chepare)
class CheparetaAdmin(admin.ModelAdmin):
    list_display = ("type", "number_of_hooks", "color", "created_by", "price")
    ordering = ("-price",)
    list_filter = ("type", "number_of_hooks", "color")
