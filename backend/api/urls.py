from django.urls import path
from . import views
from .views import EventList,EventDetail
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('events/', EventList.as_view(), name="event-list"),
    path('events/<int:pk>/', EventDetail.as_view()),
]

