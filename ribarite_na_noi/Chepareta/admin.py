from django.contrib import admin

from ribarite_na_noi.Chepareta.models import Chepare


@admin.register(Chepare)
class CheparetaAdmin(admin.ModelAdmin):
    pass
