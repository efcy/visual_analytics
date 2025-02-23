from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path("", include("user.urls")),
    path("", include("frontend.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("common.urls")),
    path("api/", include("cognition.urls")),
    path("api/", include("motion.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
