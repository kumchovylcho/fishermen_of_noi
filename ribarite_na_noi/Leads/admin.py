from django.contrib import admin

from ribarite_na_noi.Leads.models import Lead


@admin.register(Lead)
class LeadsAdmin(admin.ModelAdmin):
    pass
