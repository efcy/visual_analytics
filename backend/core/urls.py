from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("api-auth/", include("rest_framework.urls")),
    #user app uses accounts path so frontend still works
    path('accounts/', include('user.urls')),
    #frontend things where profile was used have to use accounts/ now
    #path('profile/', include('user_profile.urls')),
    path("api/", include("api.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path("", include("frontend.urls")),
]
