from django.urls import include, path
from . import views
from .AnnotationAPI import AnnotationAPI
from rest_framework import routers
from drf_spectacular.views import SpectacularSwaggerView,SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

_api_annotations_urlpatterns = [
    path('<int:pk>/', AnnotationAPI.as_view(), name='annotation-detail'),
]

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('health/',views.health_check,name="health_check"),
    path('image-count/', views.ImageCountView.as_view(), name='image-count'),
    path('annotations/', include((_api_annotations_urlpatterns, app_name), namespace='api-annotations')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.DefaultRouter()
router.register('events',views.EventViewSet)
router.register('games', views.GameViewSet)
router.register('robotdata',views.RobotDataViewSet)
router.register('image',views.ImageViewSet)
router.register("sensorlogs",views.SensorLogViewSet)

urlpatterns += router.urls
