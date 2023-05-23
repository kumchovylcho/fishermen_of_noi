from django.contrib import admin

from ribarite_na_noi.Braids.models import Braid


@admin.register(Braid)
class BraidsAdmin(admin.ModelAdmin):
    pass
