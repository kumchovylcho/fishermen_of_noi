from django.contrib import admin

from ribarite_na_noi.Reels.models import Reel


@admin.register(Reel)
class ReelsAdmin(admin.ModelAdmin):
    list_display = ("model", "gear_ratio", "size", "weight", "bearings", "created_by", "price")
    ordering = ("-price",)
    list_filter = ("model", "size", "weight", "gear_ratio")

