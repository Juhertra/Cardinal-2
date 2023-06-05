from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('', include('apps.report.urls')),
    # path('', include('apps.vulnerability.urls')),
]


