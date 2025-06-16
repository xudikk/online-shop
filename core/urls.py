from django.urls import path, include


urlpatterns = [
    path('dashboard/', include("core.dashboard.urls")),
    path('', include("core.site.urls")),
]







