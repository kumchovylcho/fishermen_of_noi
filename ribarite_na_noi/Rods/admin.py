from django.contrib import admin

from ribarite_na_noi.Rods.models import Rod


@admin.register(Rod)
class RodsAdmin(admin.ModelAdmin):
    pass
