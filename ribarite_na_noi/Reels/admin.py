from django.contrib import admin

from ribarite_na_noi.Reels.models import Reel


@admin.register(Reel)
class ReelsAdmin(admin.ModelAdmin):
    pass

