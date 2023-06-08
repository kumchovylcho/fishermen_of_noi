from django.contrib import admin

from ribarite_na_noi.Braids.models import Braid


@admin.register(Braid)
class BraidsAdmin(admin.ModelAdmin):
    list_display = ("name", "thickness", "length", "created_by", "price")
    ordering = ("-price", )
    list_filter = ("thickness", "length")