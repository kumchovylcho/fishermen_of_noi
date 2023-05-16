from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ribarite_na_noi.common.urls')),
    path('', include('ribarite_na_noi.User.urls')),
    path('rods/', include('ribarite_na_noi.Rods.urls')),
    path('reels/', include('ribarite_na_noi.Reels.urls')),
    path('braids/', include('ribarite_na_noi.Braids.urls')),
    path('chepareta/', include('ribarite_na_noi.Chepareta.urls')),

]
