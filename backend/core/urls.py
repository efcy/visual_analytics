from django.contrib import admin
from django.urls import include, path
from api.views import CreateUserView
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api-auth/", include("rest_framework.urls")),
    #user app uses accounts path so frontend still works
    path('accounts/', include('user.urls')),
    #frontend things where profile was used have to use accounts/ now
    #path('profile/', include('user_profile.urls')),
    path("api/", include("api.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
]
