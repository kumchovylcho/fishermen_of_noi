from django.contrib import admin

from ribarite_na_noi.Leads.models import Lead


@admin.register(Lead)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ("lead_type", "grams", "created_by", "price")
    ordering = ("-price",)
    list_filter = ("lead_type", "grams")
