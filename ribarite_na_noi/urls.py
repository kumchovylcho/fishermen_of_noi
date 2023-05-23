from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (path,
                         include,
                         )
from ribarite_na_noi.common.views import PageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ribarite_na_noi.common.urls')),
    path('', include('ribarite_na_noi.User.urls')),
    path('rods/', include('ribarite_na_noi.Rods.urls')),
    path('reels/', include('ribarite_na_noi.Reels.urls')),
    path('braids/', include('ribarite_na_noi.Braids.urls')),
    path('chepareta/', include('ribarite_na_noi.Chepareta.urls')),
    path('leads/', include('ribarite_na_noi.Leads.urls')),
    path('404/', PageNotFound.as_view(), name='404'),
]

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT
                      )

handler404 = PageNotFound.as_view()