from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('', include('user.urls')),
    path("api/", include("api.urls")),
    path("api/", include("cognition.urls")),
    path("api/", include("motion.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("", include("frontend.urls")),
]
